# -*- coding: utf-8 -*-

import glue as mw

def handler_message (msg):
    print msg

def main ():
    sub = mw.get_subscriber()
    
    sub.delegate(handler_message)
    sub.subscribe('saludo')
    
    t = sub.listen_new_thread(True)
    
    t.join()
  
if __name__ == '__main__':
    main()
