from encoding import Encoder

import pickle

class PickleEncoder(Encoder):
    def __init__(self):
        pass
    
    def loads(self, message):
        return pickle.loads(message)
    
    def dumps(self, message):
        return pickle.dumps(message)
    
