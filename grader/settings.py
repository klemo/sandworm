#------------------------------------------------------------------------------
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------

QUEUE_OUT = 'sandworm-q-out'
QUEUE_IN = 'sandworm-q-in'

UPLOAD_DIR = 'tmp'

SERVER = {
    'local': {
        'port': 8080,
        'mongoport': 27017,
        'mongoauth': False,
        'debug': True
        },
    'production': {
        'port': 12534,
        'mongoport': 19806,
        'mongoauth': True,
        'mongouser': '',
        'mongopassword': '',
        'debug': False
        },
    }

ENV = SERVER['local']
