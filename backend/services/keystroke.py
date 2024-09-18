import json
from typing import Optional, List

import torch
from services.auth import _create_jwt_token
from model.keystroke_verify import KeyStrokeVerifySession
from database.user_table import UserTable
from model.user import UserSchema
from model.embedding import EmbeddingSchema
from database.embedding_table import EmbeddingTable
from database.db import conn
from model.keystroke_response import KeyStrokeResponse, KeyStrokeVerifyResponse
from model.stroke import KeyStrokeInfo
from typeformer.model.Model import HARTrans
from typeformer.load import Transformer
from model.keystroke_session import KeyStrokeSession

def keywise_feature_generator():
    features = []
    last_down_idx = {}
    def next_feature(event_type: str, key: int, timestamp: float):
        nonlocal features
        if event_type == 'D':
            last_down_idx[key] = len(features)
            features.append(
                {
                    'key': key,
                    'down': timestamp,
                    'up': 0.0,
                }
            )
            yield {}
        else:
            if key not in last_down_idx or last_down_idx[key] >= len(features):
                yield {}
            features[last_down_idx[key]]['up'] = timestamp
            yield features[last_down_idx[key]]
    return next_feature

# hold latency, inter-key latency, press latency, release latency, ascii
def create_feator_vector(feature, previous_feature=None):
    if previous_feature is None:
        return torch.tensor(
            [feature['up'] - feature['down'],
             0.0,
             0.0,
             0.0,
             feature['key'] / 128] 
        )
    
    return torch.tensor(
        [feature['up'] - feature['down'],
         feature['down'] - previous_feature['up'],
         feature['down'] - previous_feature['down'],
         feature['up'] - previous_feature['up'],
         feature['key'] / 128]
    )

def model_input_generator():
    previous_feature = None
    def next_input(feature):
        nonlocal previous_feature
        vec = create_feator_vector(feature, previous_feature)
        previous_feature = feature
        yield vec
    
    return next_input

def mean_of_vectors(t: torch.Tensor) -> torch.Tensor:
    return t.mean(dim=0)

class KeyStrokeHandler:
    phrase_embeddings: List[torch.Tensor]
    session_id: Optional[int] = -1
    user_id: Optional[int] = -1
    transformer: HARTrans
    user: Optional[UserSchema] = None
    keywise_feature_generator: callable
    model_input_generator: callable
    embedding_table: EmbeddingTable
    user_table: UserTable
    
    def __init__(self, keystroke_session: KeyStrokeSession = None):
        if keystroke_session is not None:
            self._reset_ids(keystroke_session)
            
        self.phrase_embeddings = []
        self.transformer = Transformer.get()
        self.keywise_feature_generator = keywise_feature_generator()
        self.model_input_generator = model_input_generator()
        self.embedding_table = EmbeddingTable(conn())
        self.user_table = UserTable(conn())
        
    
    
    def session_handler(self, keystroke_session: KeyStrokeSession):
        response = KeyStrokeResponse(status="OK")
        if keystroke_session.mode == "INIT":
            print("Initiating session")
            self._reset_ids(keystroke_session)
            self._reset_generator()
            self._fetch_user()
        elif keystroke_session.mode == "NEXT":
            print("Saving phrase embeddings mean")
            self._save_embeddings()
            self._reset_generator()
        elif keystroke_session.mode == "STROKE":
            self._eval_embedding(keystroke_session.payload)
        elif keystroke_session.mode == "END":
            print("Saving phrase embeddings mean")
            self._save_embeddings()
        else:
            response = KeyStrokeResponse(status="ERROR", message=f"Invalid mode {keystroke_session.mode}")
            
        return response
    
    def _fetch_user(self):
        user = self.user_table.get_by_id(self.user_id)
        if user is None:
            raise Exception("User not found")
        self.user = user
    
    def _reset_ids(self, keystroke_session: KeyStrokeSession):
        self.session_id = keystroke_session.session_id
        self.user_id = keystroke_session.user_id
        
    
    def _reset_generator(self):
        self.keywise_feature_generator = keywise_feature_generator()
        self.model_input_generator = model_input_generator()

    def _update_user_signup_completion(self):
        completed = self.user.signup_phrases_completed + 1
        if completed >= self.user.signup_phrases_target:
            self.user.signup_status = "COMPLETED"
        self.user.signup_phrases_completed = completed
        self.user_table.update(self.user_id, self.user)

    def _save_embeddings(self):
        if len(self.phrase_embeddings) > 0:
            condensed_embedding = mean_of_vectors(torch.stack(self.phrase_embeddings))[0, :]
            embeddingSchema = EmbeddingSchema(embedding=condensed_embedding.tolist(), user_id=self.user_id, purpose="SIGNUP")
            self.embedding_table.insert_one(embeddingSchema)
            self._update_user_signup_completion()
        self.phrase_embeddings = []
    
    def _eval_embedding(self, payload: str):
        try:
            payload_obj = json.loads(payload)
            keystrokeInfo = KeyStrokeInfo(**payload_obj)
            f = next(self.keywise_feature_generator(
                keystrokeInfo.event_type,
                keystrokeInfo.key,
                keystrokeInfo.timestamp
            ))
            if len(f) == 0:
                return KeyStrokeResponse(status="OK")
            
            inp = next(self.model_input_generator(f))
            with torch.no_grad():
                out = self.transformer(torch.stack([inp]))
                self.phrase_embeddings.append(out)
                return KeyStrokeResponse(status="OK")
        except Exception as e:
            print(e)
            raise Exception(str(e))
        
        
class VerifyKeyStrokeHandler:
    phrase_embeddings: List[torch.Tensor]
    confidence: Optional[float] = 0.0
    username: Optional[str] = ""
    user_id: Optional[int] = -1
    user: Optional[UserSchema] = None
    transformer: HARTrans
    user: Optional[UserSchema] = None
    phrase_done = 0
    phrase_required = 3
    match_samples = 5
    matching_threshold = 0.05
    total_embeddings = 0
    matched_embeddings = 0
    keywise_feature_generator: callable
    model_input_generator: callable
    embedding_table: EmbeddingTable
    user_table: UserTable
    
    def __init__(self):
        self.phrase_embeddings = []
        self.transformer = Transformer.get()
        self.keywise_feature_generator = keywise_feature_generator()
        self.model_input_generator = model_input_generator()
        self.embedding_table = EmbeddingTable(conn())
        self.user_table = UserTable(conn())
        
    def _reset_ids(self, keystroke_verify_session: KeyStrokeVerifySession):
        self.username = keystroke_verify_session.username
    
    def _reset_metrics(self):
        self.confidence = 0.0
        self.total_embeddings = 0
        self.matched_embeddings = 0
        self.phrase_done = 0
    
    def _reset_generator(self):
        self.keywise_feature_generator = keywise_feature_generator()
        self.model_input_generator = model_input_generator()
        
    def _fetch_user(self):
        if self.username is None or len(self.username) == 0:
            raise Exception("Username not set")
        user = self.user_table.find_by_username(self.username)
        if user is None:
            raise Exception("User not found")
        self.user = user
        self.user_id = user.id
        
    def _eval_embedding(self, payload: str):
        try:
            payload_obj = json.loads(payload)
            keystrokeInfo = KeyStrokeInfo(**payload_obj)
            f = next(self.keywise_feature_generator(
                keystrokeInfo.event_type,
                keystrokeInfo.key,
                keystrokeInfo.timestamp
            ))
            if len(f) == 0:
                return KeyStrokeResponse(status="OK")
            
            inp = next(self.model_input_generator(f))
            with torch.no_grad():
                out = self.transformer(torch.stack([inp]))
                self.phrase_embeddings.append(out)
                return KeyStrokeResponse(status="OK")
        except Exception as e:
            print(e)
            raise Exception(str(e))
        
    def _compare_embeddings(self):
        if len(self.phrase_embeddings) == 0:
            raise Exception("No embeddings to compare")
        
        condensed_embedding = mean_of_vectors(torch.stack(self.phrase_embeddings))[0, :]
        embeddingSchema = EmbeddingSchema(embedding=condensed_embedding.tolist(), user_id=self.user_id, purpose="VERIFY")
        top_matches, cosine_distnaces = self.embedding_table.get_closest_by_l2_norm(embeddingSchema, self.match_samples)
        for item in zip(top_matches, cosine_distnaces):
            match = item[0]
            cosine_dist = item[1]
            print(f"Embedding id: {match.id}, user_id: {match.user_id}, purpose: {match.purpose} distance: {cosine_dist}")
            self.total_embeddings += 1
            if match.user_id == self.user.id:
                if cosine_dist < self.matching_threshold:
                    self.matched_embeddings += 1
                else:
                    print(f"Embedding cosine distance {cosine_dist} is below threshold for user {self.user.username}")
        
        self.phrase_done += 1
        self.confidence = self.matched_embeddings / self.total_embeddings if self.total_embeddings > 0 else 0.0
        self.phrase_embeddings = []
    
    def _generate_jwt_token(self):
        if self.user is None:
            raise Exception("User not found")
        if self.phrase_done < self.phrase_required:
            raise Exception(f"Phrases not yet completed {self.phrase_done} of {self.phrase_required}")
        
        if self.confidence < 0.8:
            raise Exception(f"Confidence is below threshold: {self.confidence}")
        return _create_jwt_token(self.user)
    
    def verify_handler(self, keystroke_verify_session: KeyStrokeVerifySession):
        response = KeyStrokeVerifyResponse(status="OK", user_id=self.user_id, verify_confidence=self.confidence, phrase_done=self.phrase_done)
        if keystroke_verify_session.mode == "INIT":
            print("Initiating session")
            self._reset_ids(keystroke_verify_session)
            self._reset_generator()
            self._fetch_user()
            response.user_id = self.user_id
        elif keystroke_verify_session.mode == "NEXT":
            print("Comparing phrase embeddings mean")
            self._compare_embeddings()
            response.verify_confidence = self.confidence
            response.phrase_done = self.phrase_done
            try:
                response.payload = self._generate_jwt_token()
            except:
                response.payload = ""
            self._reset_generator()
        elif keystroke_verify_session.mode == "STROKE":
            self._eval_embedding(keystroke_verify_session.payload)
        elif keystroke_verify_session.mode == "END":
            print("Comparing phrase embeddings mean")
            self._compare_embeddings()
            response.verify_confidence = self.confidence
            response.phrase_done = self.phrase_done
            response.payload = self._generate_jwt_token()
            self._reset_generator()
            self._reset_metrics()
        else:
            response = KeyStrokeResponse(status="ERROR", message=f"Invalid mode {keystroke_verify_session.mode}")
        
        return response