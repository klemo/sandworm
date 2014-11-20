#------------------------------------------------------------------------------
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------

import functools
import simplejson as json

#------------------------------------------------------------------------------

PUBLIC_USER_PROPS = {
    '_id': 0,
    'password': 0
    }

#------------------------------------------------------------------------------

def get_user(db, username):
    user = db.users.find_one({'username': username}, PUBLIC_USER_PROPS)
    return user

#------------------------------------------------------------------------------

def login_user(db, logindata):
    # todo: validate login data
    user = db.users.find_one({'username': logindata['username']},
                             PUBLIC_USER_PROPS)
    # todo: check password...
    if not user:
        return None, 'no such user'
    return user, None
