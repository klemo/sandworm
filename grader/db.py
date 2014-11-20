#------------------------------------------------------------------------------
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------

import functools
import simplejson as json

#------------------------------------------------------------------------------

USER_PROPS = {
    '_id': 0,
    'password': 0,
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
# Admin API
#------------------------------------------------------------------------------

def get_admin_labs(db, lab_id=None):
    # return all labs
    if not lab_id:
        return list(db.labs.find({}))
    # return lab_id details with results
    lab = db.labs.find_one({'id': lab_id})
    results = db.results.find_one({'id': lab_id})
    lab.update(results)
    return lab

#------------------------------------------------------------------------------
# User API
#------------------------------------------------------------------------------

def get_labs(db, user, lab_id=None):
    '''
    Retrieves all labs that are linked to user. Includes user specific data.
    '''

    def get_user_lab(_id):
        for i in user_labs:
            if i['id'] == _id:
                return i['submitted']
        return None
    
    # return all labs
    user_labs = user['labs']
    if not lab_id:
        # get all labs that belong to user
        lab_ids = [i['id'] for i in user_labs]
        labs = list(db.labs.find({'id': {'$in': lab_ids}}))
        # merge user data
        for lab in labs:
            lab['submitted'] = get_user_lab(lab['id']) or False
        return labs

    return None
