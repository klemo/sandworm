#------------------------------------------------------------------------------
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------

import functools
import simplejson as json

#------------------------------------------------------------------------------

def jsonify(req, data):
    req.set_header('Content-Type', 'application/json')
    req.write(json.dumps(data))

#------------------------------------------------------------------------------

def auth(method):
    '''
    Custom auth handler
    '''
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            self.set_status(400)
            jsonify(self, {'error': 'not authenticated'})
            return
        return method(self, *args, **kwargs)
    return wrapper
