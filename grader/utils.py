#------------------------------------------------------------------------------
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------

import functools
import pymongo
import argparse
import simplejson as json
from bson import json_util
import settings

#------------------------------------------------------------------------------

def jsonify(req, data):
    req.set_header('Content-Type', 'application/json')
    req.write(json.dumps(data, default=json_util.default))

#------------------------------------------------------------------------------

def auth(role='user'):
    def authenticate(method):
        '''
        Custom auth handler
        '''
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            if not self.current_user:
                self.set_status(400)
                jsonify(self, {'error': 'not authenticated'})
                return
            if self.current_user['role'] <> role:
                jsonify(self, {'error': 'not authorized'})
                return
            return method(self, *args, **kwargs)
        return wrapper
    return authenticate

#------------------------------------------------------------------------------

def connect_to_mongo(env):
    '''
    Use this function to connect to mongo database
    '''
    try:
        client = pymongo.MongoClient('localhost', port=env['mongoport'])
        db = client['sandworm']
        if env['mongoauth']:
            db.authenticate(env['mongouser'], env['mongopassword'])
        return db
    except Exception as e:
        print('Mongo: ', e)
    return None

#------------------------------------------------------------------------------

def load_fixtures(collections=['users', 'labs', 'results']):
    '''
    Loads fixture data to db (users...)
    '''
    print('Load fixtures')
    db = connect_to_mongo(settings.ENV)
    for c in collections:
        print(' adding {}'.format(c))
        db[c].drop()
        with open('test/fixtures/{}.json'.format(c), 'r') as f:
            items = json.loads(f.read())
            for i in items:
                db[c].insert(i)

#------------------------------------------------------------------------------

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='misc utils')
    parser.add_argument('--fixtures', help='load fixtures', default=False,
                        const='True', nargs='?')

    args = parser.parse_args()
    if args.fixtures:
        load_fixtures()
