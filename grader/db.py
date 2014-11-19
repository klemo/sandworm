#------------------------------------------------------------------------------
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------

import functools
import simplejson as json

#------------------------------------------------------------------------------

def get_user(username):
    role = 'user'
    if username == 'admin':
        role = 'admin'
    return {'username': username,
            'role': role}
