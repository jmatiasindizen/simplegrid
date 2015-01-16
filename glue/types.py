# -*- coding: utf-8 -*-

class Client (object):
    pass

class Server (object):
    def stop ( self ):
        raise NotImplementedError

    def listen ( self ):
        raise NotImplementedError

    def listen_new_thread (self,start = False):
        """ Executes Listen method in a new thread and return thread object"""
        import threading
        t = threading.Thread(target = self.listen)
        if start: 
            t.start()
            
        return t
    
class Publisher (Client):
    def __init__(self):
        pass
        
    def publish ( self, obj, subject = None ):
        raise NotImplementedError

class Subscriber (Server):
    def __init__(self):
        pass
        
    def subscribe (self, subject):
        raise NotImplementedError
        
    def unsubscribe (self, subject):
        raise NotImplementedError
        
    def delegate (self, delegate_function):
        raise NotImplementedError
        
class Producer(Client):
    def __init__(self):
        pass
    def produce(self):
        pass

class Consumer(Server):
    def __init__(self):
        pass
    def consume(self):
        pass
        
class Handler:
    def __init__(self):
        pass
        
    def get_subscriber (self):
        raise NotImplementedError
        
    def get_publisher (self):
        raise NotImplementedError
         
    def get_producer (self) :
        raise NotImplementedError
        
    def get_consumer (self):
        raise NotImplementedError
