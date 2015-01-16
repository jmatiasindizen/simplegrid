
class Encoder(object):
    def __init__(self):
        pass
    def loads(self, message):
        pass
    def dumps(self, message):
        pass

def get_encoder(encoding_protocol='Pickle', **args):
    ENCODERS = {'Pickle': 'pickle_encoder'}
    if ENCODERS.has_key(encoding_protocol):
        exec('import ' + ENCODERS[encoding_protocol])
        exec('encoder = ' + ENCODERS[encoding_protocol] + '.' + str(encoding_protocol) + 'Encoder()')
        return encoder
    else:
        return None
