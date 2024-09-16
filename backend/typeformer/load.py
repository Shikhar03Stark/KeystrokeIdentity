import torch
from typeformer.model.Model import HARTrans
from typeformer.config.train_config import configs

class Transformer:
    _instance = None
    
    def get():
        if Transformer._instance is not None:
            return Transformer._instance
        typeformer_state = torch.load('TypeFormer_pretrained.pt', map_location='cpu', weights_only=True)
        altered_state = { key.replace('.net.3', '.net.2').replace('net','ff'): value for key, value in typeformer_state.items()}
        transformer = HARTrans(configs).double()
        transformer.load_state_dict(altered_state, strict=True)
        Transformer._instance = transformer
        print("Transformer loaded")
        return Transformer._instance
    