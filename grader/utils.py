#------------------------------------------------------------------------------
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------

import functools
import pymongo
import redis
import logging
import argparse
import simplejson as json
from bson import json_util
import settings

#------------------------------------------------------------------------------

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)

#------------------------------------------------------------------------------

def jsonify(req, data):
    req.set_header('Content-Type', 'application/json')
    req.write(json.dumps(data, default=json_util.default))

#------------------------------------------------------------------------------

def auth(role=None, websock=False):
    def authenticate(method):
        '''
        Custom auth handler
        '''
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            if not self.current_user:
                self.set_status(400)
                if not websock:
                    jsonify(self, {'error': 'not authenticated'})
                else:
                    LOGGER.error('WS not authenticated')
                return
            if role and self.current_user['role'] <> role:
                if not websock:
                    jsonify(self, {'error': 'not authorized'})
                else:
                    LOGGER.error('WS not authorized')
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

def connect_to_redis(env):
    '''
    Use this function to connect to redis
    '''
    try:
        r = redis.StrictRedis(host='localhost',
                              port=env['redisport'],
                              db=0)
        r.ping()
        return r
    except Exception as e:
        print('Redis ', e)
    return None

#------------------------------------------------------------------------------

def load_fixtures():
    '''
    Loads fixture data to db (users...)
    '''
    print('Load fixtures')
    collections = ['users', 'labs', 'results', 'user_results', 'all_results']
    db = connect_to_mongo(settings.ENV)
    for c in collections:
        print(' adding {}'.format(c))
        db[c].drop()
        with open('test/fixtures/{}.json'.format(c), 'r') as f:
            items = json_util.loads(f.read())
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
