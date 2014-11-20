#------------------------------------------------------------------------------
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------

import functools
import simplejson as json

#------------------------------------------------------------------------------

USER_PROPS = {
    '_id': 0,
    'password': 0
    }

#------------------------------------------------------------------------------

def get_user(db, username):
    user = db.users.find_one({'username': username}, USER_PROPS)
    return user

#------------------------------------------------------------------------------

def login_user(db, logindata):
    # todo: validate login data
    user = db.users.find_one({'username': logindata['username']}, USER_PROPS)
    # todo: check password...
    if not user:
        return None, 'no such user'
    return user, None

#------------------------------------------------------------------------------

def get_admin_labs(db, lab_id=None):
    # return all labs
    if not lab_id:
        return db.labs.find({})
    # return lab_id details with results
    lab = db.labs.find_one({'id': lab_id})
    results = db.results.find_one({'id': lab_id})
    lab.update(results)
    return lab
