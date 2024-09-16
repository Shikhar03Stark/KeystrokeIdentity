import json
from typing import Optional, List

import torch
from model.keystroke_response import KeyStrokeResponse
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
    keywise_feature_generator: callable
    model_input_generator: callable
    
    def __init__(self, keystroke_session: KeyStrokeSession = None):
        if keystroke_session is not None:
            self.session_id = keystroke_session.session_id
            self.user_id = keystroke_session.user_id
            
        self.phrase_embeddings = []
        self.transformer = Transformer.get()
        self.keywise_feature_generator = keywise_feature_generator()
        self.model_input_generator = model_input_generator()
    
    
    def session_handler(self, keystroke_session: KeyStrokeSession):
        response = KeyStrokeResponse(status="OK")
        if keystroke_session.mode == "INIT":
            print("Initiating session")
            self._reset_ids(keystroke_session)
            self._reset_generator()
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
    
    def _reset_ids(self, keystroke_session: KeyStrokeSession):
        self.session_id = keystroke_session.session_id
        self.user_id = keystroke_session.user_id
    
    def _reset_generator(self):
        self.keywise_feature_generator = keywise_feature_generator()
        self.model_input_generator = model_input_generator()

    def _save_embeddings(self):
        if len(self.phrase_embeddings) > 0:
            condensed = mean_of_vectors(torch.stack(self.phrase_embeddings))
            print(condensed)
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
            return KeyStrokeResponse(status="ERROR", message=str(e))