# -*- coding: utf-8 -*-

import glue as mw

def main ():
    prod = mw.get_producer()

    prod.produce('despedida', 'Adios mundo')
    
if __name__ == '__main__':
    main()

