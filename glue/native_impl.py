# -*- coding: utf-8 -*-

from types import Handler, Subscriber, Publisher, Consumer, Producer
import redis
import threading

class NativeHandler ( Handler ): 
    def __init__(self):
        pass
        
    def get_subscriber(self, **args):
        return NativeSubscriber(args['QUEUE'])
        
    def get_publisher(self, **args):
        return NativePublisher(args['QUEUE'])
        
    def get_producer(self, **args):
        return NativeProducer(args['QUEUE'])
        
    def get_consumer(self, **args):
        return NativeConsumer(args['QUEUE'])

class NativeSubscriber (Subscriber):
    def __init__(self, queue):
        self.queue = queue
        
    def subscribe (self, subject):
        pass
        
    def unsubscribe (self):
        pass
        
    def delegate (self, delegate_function):
        pass
        
    def listen (self):
        pass
    
class NativePublisher (Publisher):
    def __init__(self, queue):
        self.queue = queue
        
    def publish(self, subject, message):
        pass

class NativeProducer (Producer):
    def __init__(self, queue):
        self.queue = queue
        
    def produce(self, subject, data):
        pass

class NativeConsumer (Consumer):
    def __init__(self, queue):
        self.queue = queue
        
    def consume(self, subject, block=True):
        pass


