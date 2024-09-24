import random
from typing import List

class PhraseCollection:
    filepath: str = "phrases.txt"
    phrases: List[str] = []
    
    def load_file():
        if len(PhraseCollection.phrases) == 0:
            print("Loading phrases from file")
            with open(PhraseCollection.filepath, "r") as file:
                for line in file:
                    PhraseCollection.phrases.append(line.strip())
                    
    def get_phrases(limit: int = 5):
        PhraseCollection.load_file()
        return random.sample(PhraseCollection.phrases, min(limit, len(PhraseCollection.phrases)))

        
    