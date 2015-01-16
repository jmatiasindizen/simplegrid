from multiprocessing import cpu_count, Process
from datetime import datetime
from time import sleep
import ConfigParser
import glue as mw
import messages as msg
from worker import Worker

AGENT_CONNECTION = 'AGENT_CONNECTION'
AGENT_REQUEST_SUBJECT = 'REQUEST_SUBJECT'
AGENT_RESPONSE_SUBJECT = 'RESPONSE_SUBJECT'

MISCELLANEOUS = 'MISC'
INIT_RESPONSE_TIMEOUT = 'INIT_RESPONSE_TIMEOUT'
START_RESPONSE_TIMEOUT = 'START_RESPONSE_TIMEOUT'
STOP_RESPONSE_TIMEOUT = 'STOP_RESPONSE_TIMEOUT'
RESTART_RESPONSE_TIMEOUT = 'RESTART_RESPONSE_TIMEOUT'
UPDATE_RESPONSE_TIMEOUT = 'UPDATE_RESPONSE_TIMEOUT'
HEARTBEAT_RESPONSE_TIMEOUT = 'HEARTBEAT_RESPONSE_TIMEOUT'

class Monitor(object):
    
    def __init__(self, cfg_path):
        #Get config
        
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
        
        self.get_config(cfg_path)
        
        #Set Response Timeouts
        self.init_response_timeout = self.config.get(MISCELLANEOUS, INIT_RESPONSE_TIMEOUT)
        self.start_response_timeout = self.config.get(MISCELLANEOUS, START_RESPONSE_TIMEOUT)
        self.stop_response_timeout = self.config.get(MISCELLANEOUS, STOP_RESPONSE_TIMEOUT)
        self.restart_response_timeout = self.config.get(MISCELLANEOUS, RESTART_RESPONSE_TIMEOUT)
        self.update_response_timeout = self.config.get(MISCELLANEOUS, UPDATE_RESPONSE_TIMEOUT)
        self.heartbeat_response_timeout = self.config.get(MISCELLANEOUS, HEARTBEAT_RESPONSE_TIMEOUT)
        
        #Get pub/sub topics
        self.agents_request_subject = self.config.get(AGENT_CONNECTION, AGENT_REQUEST_SUBJECT)
        self.agents_response_subject = self.config.get(AGENT_CONNECTION, AGENT_RESPONSE_SUBJECT)
        
        #Get Publisher to agents requests
        self.pub_agents = mw.get_publisher()
        
        #Get Subscriber to agents responses
        self.sub_agents = mw.get_subscriber()
        self.sub_agents.delegate(self.manage_response_messages)
        self.sub_agents.subscribe(self.agents_response_subject)

        #Start a thread which listening agents response messages
        t = self.sub_agents.listen_new_thread()
        t.start()
        
    def get_config(self, cfg_path):
        self.config = ConfigParser.ConfigParser()
        self.config.read(cfg_path)
                   
    def manage_response_messages(self, message):
        print str(message)
        if message['type'] == 'message':
            if self.response_messages_handler.has_key(message['data'].kind_message):
                self.response_messages_handler[message['data'].kind_message](message['data'])
            else:
                print 'The operation is not implemented'
        else:
            print 'It is not a message'
        
    def init_response(self, message):
        if self.responses_cache['INIT.RESPONSE'].has_key(message.timestamp):
            self.responses_cache['INIT.RESPONSE'][message.timestamp].append((message.response_id,message.worker_ids))
        else:
            print 'Agent ' + message.response_id + ' exceed timeout for init response' 
    
    def start_response(self, message):
        if self.responses_cache['START.RESPONSE'].has_key(message.timestamp):
            self.responses_cache['START.RESPONSE'][message.timestamp].append(message.response_id)
        else:
            print 'Agent ' + message.response_id + ' exceed timeout for start response' 

    def stop_response(self, message):
        if self.responses_cache['STOP.RESPONSE'].has_key(message.timestamp):
            self.responses_cache['STOP.RESPONSE'][message.timestamp].append(message.response_id)
        else:
            print 'Agent ' + message.response_id + ' exceed timeout for stop response' 

    def restart_response(self, message):
        if self.responses_cache['RESTART.RESPONSE'].has_key(message.timestamp):
            self.responses_cache['RESTART.RESPONSE'][message.timestamp].append(message.response_id)
        else:
            print 'Agent ' + message.response_id + ' exceed timeout for restart response' 

    def update_response(self, message):
        if self.responses_cache['UPDATE.RESPONSE'].has_key(message.timestamp):
            self.responses_cache['UPDATE.RESPONSE'][message.timestamp].append(message.response_id)
        else:
            print 'Agent ' + message.response_id + ' exceed timeout for update response' 

    def heartbeat_response(self, message):
        if self.responses_cache['HEARTBEAT.RESPONSE'].has_key(message.timestamp):
            self.responses_cache['HEARTBEAT.RESPONSE'][message.timestamp].append((message.response_id,message.worker_ids))
        else:
            print 'Agent ' + message.response_id + ' exceed timeout for heartbeat response' 

    def init(self, agent_ids):
        
        timestamp = str(datetime.today())
        
        self.responses_cache['INIT.RESPONSE'][timestamp] = []
        
        #Send request to my agents
        request_message = msg.InitRequestMessage(timestamp)
        self.pub_agents.publish(self.agents_request_subject, request_message)
        
        #Waiting responses from agents
        sleep(1)#self.heartbeat_response_timeout)
        
        alive_agents_ids = self.responses_cache['INIT.RESPONSE'][timestamp]
        del self.responses_cache['INIT.RESPONSE'][timestamp]
        
        #alive_agents_ids contains created agents ids and related worker ids for each agent
        
        return alive_agents_ids
    
    def start(self):
        pass
    
    def stop(self):
        pass
    
    def restart(self):
        pass
    
    def update(self):
        pass
    
    def heartbeat(self):
        
        timestamp = str(datetime.today())
        
        self.responses_cache['HEARTBEAT.RESPONSE'][timestamp] = []
        
        #Send request to my agents
        request_message = msg.HeartbeatRequestMessage(timestamp)
        self.pub_workers.publish(self.workers_request_subject, request_message)
        
        #Waiting responses from workers
        sleep(1)#self.heartbeat_response_timeout)
        
        alive_agents_ids = self.responses_cache['HEARTBEAT.RESPONSE'][timestamp]
        del self.responses_cache['HEARTBEAT.RESPONSE'][timestamp]
        
        print 'Alive agents:' + ', '.join(alive_worker_ids)
        
        #alive_agents_ids contains agents ids and related worker ids for each agent
        
        return alive_agents_ids

if __name__ == '__main__':
    monitor = Monitor('../cfg/monitor.cfg')
    monitor.heartbeat('')
    #broker.init()
    import pdb
    pdb.set_trace()

