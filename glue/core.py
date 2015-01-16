# -*- coding: utf-8 -*-

from types import Handler

def get_handler(protocol='Redis', **args):
    HANDLERS = {'Redis': 'redis_impl'}
    if HANDLERS.has_key(protocol):
        exec('import ' + HANDLERS[protocol])
        exec('handler = ' + HANDLERS[protocol] + '.' + str(protocol) + 'Handler()')
        return handler
    else:
        return None

def get_subscriber(protocol='Redis', encoding_protocol='pickle', **args):
    handler = get_handler(protocol)
    if handler:
        return handler.get_subscriber(encoding_protocol)
    else:
        return None

def get_publisher(protocol='Redis', encoding_protocol='pickle', **args):
    handler = get_handler(protocol)
    if handler:
        return handler.get_publisher(encoding_protocol)
    else:
        return None

def get_producer(protocol='Redis', **args):
    handler = get_handler(protocol)
    if handler:
        return handler.get_producer()
    else:
        return None

def get_consumer(protocol='Redis', **args):
    handler = get_handler(protocol)
    if handler:
        return handler.get_consumer()
    else:
        return None
