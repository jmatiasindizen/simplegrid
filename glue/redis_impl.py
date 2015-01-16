# -*- coding: utf-8 -*-

from types import Handler, Subscriber, Publisher, Consumer, Producer
from msg.encoding import get_encoder
import redis
import threading

class RedisHandler ( Handler ): 
    def __init__(self):
        pass
        
    def get_subscriber(self, encoding_protocol):
        redis_connection = redis.Redis()
        return RedisSubscriber(redis_connection, encoding_protocol)
        
    def get_publisher(self, encoding_protocol):
        redis_connection = redis.Redis()
        return RedisPublisher(redis_connection, encoding_protocol)
        
    def get_producer(self):
        redis_connection = redis.Redis()
        return RedisProducer(redis_connection)
        
    def get_consumer(self):
        redis_connection = redis.Redis()
        return RedisConsumer(redis_connection)

class RedisSubscriber (Subscriber):
    def __init__(self, redis_connection, encoding_protocol):
        self.redis_connection = redis_connection
        self.encoding_protocol = encoding_protocol
        self.pubsub = self.redis_connection.pubsub()
        
    def subscribe (self, subject):
        self.pubsub.subscribe(subject)
        
    def unsubscribe (self):
        self.pubsub.unsubscribe()
        
    def delegate (self, delegate_function):
        self.delegate_function = delegate_function
        
    def listen (self):
        for msg in self.pubsub.listen():
            #import pickle
            #if msg['type'] == 'message':
            #    msg['data'] = pickle.loads(msg['data'])
            encoder = get_encoder(self.encoding_protocol)
            if msg['type'] == 'message':
                msg['data'] = encoder.loads(msg['data'])
            self.delegate_function(msg)
    
class RedisPublisher (Publisher):
    def __init__(self, redis_connection, encoding_protocol):
        self.redis_connection = redis_connection
        self.encoding_protocol = encoding_protocol
        
    def publish(self, subject, message):
        #import pickle
        #encoded_message = pickle.dumps(message)
        encoder = get_encoder(self.encoding_protocol)
        encoded_message = encoder.dumps(message)
        self.redis_connection.publish(subject, encoded_message)

class RedisProducer (Producer):
    def __init__(self, redis_connection):
        self.redis_connection = redis_connection
        
    def produce(self, subject, data):
        self.redis_connection.rpush(subject, data)

class RedisConsumer (Consumer):
    def __init__(self, redis_connection):
        self.redis_connection = redis_connection
        
    def consume(self, subject, block=True):
        if block:
            item = self.redis_connection.blpop(subject)
        else:
            item = self.redis_connection.lpop(subject)
        return item


