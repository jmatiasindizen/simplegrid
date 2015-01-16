# -*- coding: utf-8 -*-

import glue as mw

def main ():
    pub = mw.get_publisher()

    pub.publish('ejemplo1', 'INIT')
    pub.publish('ejemplo1', 'START')
    pub.publish('ejemplo1', 'STOP')
    pub.publish('ejemplo1', 'RESTART2')
    
if __name__ == '__main__':
    main()

