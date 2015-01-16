from multiprocessing import cpu_count, Process
from datetime import datetime
from time import sleep
from socket import gethostbyname, gethostname
import ConfigParser
import glue as mw
import messages as msg
from worker import Worker

MONITOR_CONNECTION = 'MONITOR_CONNECTION'
MONITOR_REQUEST_SUBJECT = 'REQUEST_SUBJECT'
MONITOR_RESPONSE_SUBJECT = 'RESPONSE_SUBJECT'

WORKERS_CONNECTION = 'WORKERS_CONNECTION'
WORKERS_REQUEST_SUBJECT = 'REQUEST_SUBJECT'
WORKERS_RESPONSE_SUBJECT = 'RESPONSE_SUBJECT'

MISCELLANEOUS = 'MISC'
INIT_RESPONSE_TIMEOUT = 'INIT_RESPONSE_TIMEOUT'
START_RESPONSE_TIMEOUT = 'START_RESPONSE_TIMEOUT'
STOP_RESPONSE_TIMEOUT = 'STOP_RESPONSE_TIMEOUT'
RESTART_RESPONSE_TIMEOUT = 'RESTART_RESPONSE_TIMEOUT'
UPDATE_RESPONSE_TIMEOUT = 'UPDATE_RESPONSE_TIMEOUT'
HEARTBEAT_RESPONSE_TIMEOUT = 'HEARTBEAT_RESPONSE_TIMEOUT'

class Agent(object):
    
    def __init__(self, cfg_path):
        #Get config
        self.request_messages_handler = {'INIT.REQUEST': self.init_request,
                                         'START.REQUEST': self.start_request,
                                         'STOP.REQUEST': self.stop_request,
                                         'RESTART.REQUEST': self.restart_request,
                                         'UPDATE.REQUEST': self.update_request,
                                         'HEARTBEAT.REQUEST': self.heartbeat_request }
        
        self.response_messages_handler = {'INIT.RESPONSE': self.init_response,
                                          'START.RESPONSE': self.start_response,
                                          'STOP.RESPONSE': self.stop_response,
                                          'RESTART.RESPONSE': self.restart_response,
                                          'UPDATE.RESPONSE': self.update_response,
                                          'HEARTBEAT.RESPONSE': self.heartbeat_response }
        
        self.responses_cache = {'INIT.RESPONSE': {},
                                'START.RESPONSE': {},
                                'STOP.RESPONSE': {},
                                'RESTART.RESPONSE': {},
                                'UPDATE.RESPONSE': {},
                                'HEARTBEAT.RESPONSE': {} }
        
        #agent_id will be ip address hostname
        self.agent_id = gethostbyname(gethostname())
        self.get_config(cfg_path)
        
        #Set Response Timeouts
        self.init_response_timeout = self.config.get(MISCELLANEOUS, INIT_RESPONSE_TIMEOUT)
        self.start_response_timeout = self.config.get(MISCELLANEOUS, START_RESPONSE_TIMEOUT)
        self.stop_response_timeout = self.config.get(MISCELLANEOUS, STOP_RESPONSE_TIMEOUT)
        self.restart_response_timeout = self.config.get(MISCELLANEOUS, RESTART_RESPONSE_TIMEOUT)
        self.update_response_timeout = self.config.get(MISCELLANEOUS, UPDATE_RESPONSE_TIMEOUT)
        self.heartbeat_response_timeout = self.config.get(MISCELLANEOUS, HEARTBEAT_RESPONSE_TIMEOUT)
        
        #Get pub/sub topics
        self.monitor_request_subject = self.config.get(MONITOR_CONNECTION, MONITOR_REQUEST_SUBJECT)
        self.monitor_response_subject = self.config.get(MONITOR_CONNECTION, MONITOR_RESPONSE_SUBJECT)
        self.workers_request_subject = self.config.get(WORKERS_CONNECTION, WORKERS_REQUEST_SUBJECT)
        self.workers_response_subject = self.config.get(WORKERS_CONNECTION, WORKERS_RESPONSE_SUBJECT)
        
        #Get Publisher to workers requests
        self.pub_workers = mw.get_publisher()
        
        #Get Subscriber to workers responses
        self.sub_workers = mw.get_subscriber()
        self.sub_workers.delegate(self.manage_response_messages)
        self.sub_workers.subscribe(self.workers_response_subject)

        #Start a thread which listening worker response messages
        t = self.sub_workers.listen_new_thread()
        t.start()
        
        #Get Publisher to monitor responses
        self.pub_workers = mw.get_publisher()
               
        #Get Subscriber to monitor requests
        self.sub_monitor = mw.get_subscriber()
        self.sub_monitor.delegate(self.manage_request_messages)
        self.sub_monitor.subscribe(self.workers_response_subject)
        
        #Start a thread which listening monitor request messages
        self.sub_monitor.listen_new_thread()

    def get_config(self, cfg_path):
        self.config = ConfigParser.ConfigParser()
        self.config.read(cfg_path)
        
    def manage_request_messages(self, message):
        print str(message)
        if message['type'] == 'message':
            if self.request_messages_handler.has_key(message['data'].kind_message):
                self.request_messages_handler[message['data'].kind_message](message['data'])
            else:
                print 'The operation is not implemented'
        else:
            print 'It is not a message'
            
    def manage_response_messages(self, message):
        print str(message)
        if message['type'] == 'message':
            if self.response_messages_handler.has_key(message['data'].kind_message):
                self.response_messages_handler[message['data'].kind_message](message['data'])
            else:
                print 'The operation is not implemented'
        else:
            print 'It is not a message'
    
    def create_worker(self):
        return Worker()
    
    def init_request(self, message):
        print 'INIT'
        
        self.responses_cache['INIT.RESPONSE'][message.current_datetime] = []
        
        #Send init message to workers
        request_message = msg.InitRequestMessage(message.current_datetime)
        self.pub_workers.publish(self.workers_request_subject, request_message)
             
        #self.num_workers = cpu_count()
        #self.pool = [Process(target=self.create_worker) for i in xrange(self.num_workers)]
        #[p.start() for p in self.pool]
        #[p.join() for p in self.pool]
        
        #
        sleep(1)
        
        alive_workers_ids = self.responses_cache['INIT.RESPONSE'][message.current_datetime]
        del self.responses_cache['INIT.RESPONSE'][message.current_datetime]
        
        #Send response to my monitor
        response_message = msg.InitResponseMessage(request_message.timestamp, self.agent_id, alive_workers_ids)
        self.pub_agent.publish(self.response_subject, response_message)

        
    def start_request(self, message):
        print 'START'
        
    def stop_request(self, message):
        print 'STOP'
        
    def restart_request(self, message):
        print 'RESTART'
        
    def update_request(self, message):
        print 'UPDATE'
        #pub = mw.get_publisher()
        #pub.publish(self.config.get(WORKERS_CONNECTION, WORKERS_SUBJECT), 'UPDATE')
        
    def heartbeat_request(self, message):
        print 'HEARTBEAT'
      
        self.responses_cache['HEARTBEAT.RESPONSE'][message.timestamp] = []
        
        #Send request to my workers
        request_message = msg.HeartbeatRequestMessage(timestamp)
        self.pub_workers.publish(self.workers_request_subject, request_message)
        
        #Waiting responses from workers
        sleep(1)#self.heartbeat_response_timeout)
        
        alive_worker_ids = self.responses_cache['HEARTBEAT.RESPONSE'][message.timestamp]
        del self.responses_cache['HEARTBEAT.RESPONSE'][message.timestamp]
        
        print 'Alive workers:' + ', '.join(alive_worker_ids)
        
        #Send heartbeat response message to my monitor
        response_message = msg.HeartbeatResponseMessage(request_message.timestamp, self.worker_id, alive_worker_ids)
        self.pub_agent.publish(self.response_subject, response_message)
        
    
    def init_response(self, message):
        if self.responses_cache['INIT.RESPONSE'].has_key(message.timestamp):
            self.responses_cache['INIT.RESPONSE'][message.timestamp].append((message.response_id,message.worker_ids))
        else:
            print 'Worker ' + message.response_id + ' exceed timeout for init response' 
    
    def start_response(self, message):
        if self.responses_cache['START.RESPONSE'].has_key(message.timestamp):
            self.responses_cache['START.RESPONSE'][message.timestamp].append(message.response_id)
        else:
            print 'Worker ' + message.response_id + ' exceed timeout for start response' 

    def stop_response(self, message):
        if self.responses_cache['STOP.RESPONSE'].has_key(message.timestamp):
            self.responses_cache['STOP.RESPONSE'][message.timestamp].append(message.response_id)
        else:
            print 'Worker ' + message.response_id + ' exceed timeout for stop response' 

    def restart_response(self, message):
        if self.responses_cache['RESTART.RESPONSE'].has_key(message.timestamp):
            self.responses_cache['RESTART.RESPONSE'][message.timestamp].append(message.response_id)
        else:
            print 'Worker ' + message.response_id + ' exceed timeout for restart response' 

    def update_response(self, message):
        if self.responses_cache['UPDATE.RESPONSE'].has_key(message.timestamp):
            self.responses_cache['UPDATE.RESPONSE'][message.timestamp].append(message.response_id)
        else:
            print 'Worker ' + message.response_id + ' exceed timeout for update response' 

    def heartbeat_response(self, message):
        if self.responses_cache['HEARTBEAT.RESPONSE'].has_key(message.timestamp):
            self.responses_cache['HEARTBEAT.RESPONSE'][message.timestamp].append((message.response_id,message.worker_ids))
        else:
            print 'Worker ' + message.response_id + ' exceed timeout for heartbeat response' 


if __name__ == '__main__':
    agent = Agent('../cfg/agent.cfg')
    agent.heartbeat_request('')
    #broker.init()
    import pdb
    pdb.set_trace()
    agent.heartbeat()

