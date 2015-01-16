from datetime import datetime
from threading import Condition
from socket import gethostbyname, gethostname
from os import getpid
import glue as mw
import messages as msg
import ConfigParser

AGENT_CONNECTION = 'AGENT_CONNECTION'
AGENT_REQUEST = 'REQUEST_SUBJECT'
AGENT_RESPONSE = 'RESPONSE_SUBJECT'

class Worker(object):
    def __init__(self, cfg_path, worker_id='NON_INIT'):
        #Get config
        self.request_messages_handler = {'INIT.REQUEST': self.init_request,
                                         'START.REQUEST': self.start_request,
                                         'STOP.REQUEST': self.stop_request,
                                         'RESTART.REQUEST': self.restart_request,
                                         'UPDATE.REQUEST': self.update_request,
                                         'HEARTBEAT.REQUEST': self.heartbeat_request }
        
        self.worker_id = gethostbyname(gethostname()) + '::' + getpid()
        self.get_config(cfg_path)
        
        self.request_subject = self.config.get(AGENT_CONNECTION, AGENT_REQUEST)
        self.response_subject = self.config.get(AGENT_CONNECTION, AGENT_RESPONSE)
        self.cons_subject = ''
              
        #Subscribe to agent requests
        self.sub_agent = mw.get_subscriber()
        self.sub_agent.delegate(self.manage_request_messages)
        self.sub_agent.subscribe( self.request_subject)
        
        t = self.sub_agent.listen_new_thread()
        t.start()
        
        #Get Publisher to agent responses
        self.pub_agent = mw.get_publisher()
        
        #START/STOP condition
        self.working_condition = Condition()
        self.working = False #worker start in stop mode
        
        #Worker state
        #self.state_condition = Condition()
        #self.state = 
        
        
    def get_config(self, cfg_path):
        self.config = ConfigParser.ConfigParser()
        self.config.read(cfg_path)
    
    def manage_request_messages(self, message):
        print str(message)
        if message['type'] == 'message':
            print str(message['data'])
            if self.request_messages_handler.has_key(message['data'].kind_message):
                self.request_messages_handler[message['data'].kind_message](message['data'])
            else:
                print 'The operation is not implemented'
        else:
            print 'It is not a message'
    
    def dispatch_tasks(self):
        cons = mw.get_consumer()
        while True:
            self.working_condition.acquire()
            while True:
                if self.working:
                    task = cons.consume(self.cons_subject)
                    
                    #Do something
                    
                    #Write result
                    break
                self.working_condition.wait()
            self.working_condition.release()
        
    
    def init_request(self, request_message):
        print 'INIT'
        
        response_message = msg.InitResponseMessage(request_message.timestamp, self.worker_id)
        self.pub_agent.publish(self.response_subject, response_message)
        
        #Come on tasks!!!
        #self.dispatch_tasks()
        
    def start_request(self, request_message):
        print 'START'
        self.working_condition.acquire()
        self.working = True
        self.working_condition.notify()
        self.working_condition.release()
        #response_message = 'START'
        #self.pub_agent.publish(self.response_subject, response_message)
        
    def stop_request(self, request_message):
        print 'STOP'
        self.working_condition.acquire()
        self.working = False
        self.working_condition.release()
        #response_message = 'STOP'
        #self.pub_agent.publish(self.response_subject, response_message)
        
    def restart_request(self, request_message):
        print 'RESTART'
        #response_message = 'RESTART'
        #self.pub_agent.publish(self.response_subject, response_message)
        
    def update_request(self, request_message):
        print 'UPDATE'
        #response_message = 'UPDATE'
        #self.pub_agent.publish(self.response_subject, response_message)
        
    def heartbeat_request(self, request_message):
        print 'HEARTBEAT'
        
        #Send heartbeat response message to my agent
        response_message = msg.HeartbeatResponseMessage(request_message.timestamp, self.worker_id)
        self.pub_agent.publish(self.response_subject, response_message)


if __name__ == '__main__':
    worker = Worker('../cfg/worker.cfg', worker_id='Worker1')
    worker = Worker('../cfg/worker.cfg', worker_id='Worker2')
    worker = Worker('../cfg/worker.cfg', worker_id='Worker3')
