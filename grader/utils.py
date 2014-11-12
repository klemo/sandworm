#------------------------------------------------------------------------------
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------

import jwt
import base64
import os
import creds

#------------------------------------------------------------------------------

def login(user):
    if user['password'] <> 'test':
        return {'error': 'invalid password'}
    del user['password']
    token = jwt.encode(user, creds.JWT_SECRET)
    return {'token': token}

#------------------------------------------------------------------------------

def authenticate(request):
    '''
    Authentication using JSON Web tokens (pyjwt)
    Loosely based on https://docs.auth0.com/server-apis/python
    '''
    auth = request.request.headers.get('Authorization', None)
    if not auth:
        return {'error': 'authorization header missing'}
    auth_parts = auth.split()
    if auth_parts[0].lower() != 'bearer':
        return {'error ': 'invalid header: must start with bearer'}
    elif len(auth_parts) == 1:
        return {'error': 'invalid header: token not found'}
    elif len(auth_parts) > 2:
        return {'error': 'invalid header: too long'}

    token = auth_parts[1]
    try:
        payload = jwt.decode(token, creds.JWT_SECRET)
    except jwt.ExpiredSignature:
        return {'error': 'token is expired'}
    except jwt.DecodeError:
        return {'error': 'token signature is invalid'}

    return payload

#------------------------------------------------------------------------------
