from datetime import datetime


class Message (object):
    def __init__(self, current_datetime):
        self.timestamp = current_datetime

class InitRequestMessage (Message):
    def __init__(self, current_datetime):
        self.timestamp = current_datetime
        self.kind_message = 'INIT.REQUEST'
        
class InitResponseMessage (Message):
    def __init__(self, current_datetime, response_id, worker_ids=[]):
        self.timestamp = current_datetime
        self.kind_message = 'INIT.RESPONSE' 
        self.response_id = response_id
        self.worker_ids = worker_ids
        
class HeartbeatRequestMessage (Message):
    def __init__(self, current_datetime):
        self.timestamp = current_datetime
        self.kind_message = 'HEARTBEAT.REQUEST'
        
class HeartbeatResponseMessage (Message):
    def __init__(self, current_datetime, response_id, worker_ids=[]):
        self.timestamp = current_datetime
        self.kind_message = 'HEARTBEAT.RESPONSE'
        self.response_id = response_id
        self.worker_ids = worker_ids
    
