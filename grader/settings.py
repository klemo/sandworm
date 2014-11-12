# -*- coding: utf-8 -*-

COOKIE_SECRET = 'kauoXgh-SEaRbpSkAChpw18AIqXR1EAZhWuv9Y7i07E='

#------------------------------------------------------------------------------

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
