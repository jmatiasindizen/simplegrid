# -*- coding: utf-8 -*-

import glue as mw

def main ():
    cons = mw.get_consumer()
    
    while True:
        print '1'
        print cons.consume('despedida')
        print '2'
  
if __name__ == '__main__':
    main()
