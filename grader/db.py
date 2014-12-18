#------------------------------------------------------------------------------
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------

import os.path
import uuid
import functools
import simplejson as json
import logging
import settings

#------------------------------------------------------------------------------

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)

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
    '''
    Returns list of labs for admin role (or single lab with lab_id)
    '''
    # return all labs
    if not lab_id:
        return list(db.labs.find({}))
    # return lab_id details with results
    lab = db.labs.find_one({'id': lab_id})
    results = db.results.find_one({'id': lab_id})
    if results:
        lab.update(results)
    return lab

#------------------------------------------------------------------------------

def get_admin_all_results(db):
    '''
    Return all results calculated in batch
    '''
    return db.all_results.find_one()

#------------------------------------------------------------------------------

def get_admin_users(db):
    '''
    Return all users
    '''
    return list(db.users.find({}, USER_PROPS))

#------------------------------------------------------------------------------

def save_admin_lab(db, lab):
    '''
    Create new lab
    '''
    # todo: validate data
    print lab
    # todo: better slug...
    lab['id'] = lab['name'].lower().replace(' ', '-')
    try:
        db.labs.insert(lab)
    except Exception as e:
        return None, 'could not save lab'
    return lab, ''

#------------------------------------------------------------------------------

def delete_admin_lab(db, lab_id):
    '''
    Deletes lab
    '''
    try:
        db.labs.remove({'id': lab_id})
    except Exception as e:
        raise 'delete failed'

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

    # return lab_id details with results
    lab = db.labs.find_one({'id': lab_id})
    results = db.user_results.find_one({'id': lab_id,
                                        'username': user['username']})
    lab.update(results)
    return lab

#------------------------------------------------------------------------------

def save_uploaded_archive(request, user):
    '''
    Saves uploaded archive to specific folder and returns final archive path
    '''
    filepost = request.files.get('file')
    fileinfo = filepost[0]
    file_name = fileinfo['filename']
    # dir path: UPLOAD_DIR/{{username}}/
    archive_dir_path = os.path.join(settings.UPLOAD_DIR,
                                    user['username'])
    if not os.path.exists(archive_dir_path):
        os.makedirs(archive_dir_path)
    archive_path = os.path.join(archive_dir_path, file_name)
    with open(archive_path, 'wb') as f:
        f.write(fileinfo['body'])
    LOGGER.info('File {} saved to {}'.format(file_name, archive_dir_path))
    return archive_path

#------------------------------------------------------------------------------

def submit_job(application, archive_path, user):
    '''
    Submits user job to message queue
    '''
    # generate unique job id
    job_id = str(uuid.uuid4())
    # TODO save this to db
    LOGGER.info('Submitting {} to queue for user {}'.format(archive_path,
                                                            user['username']))
    message = {
        'job_id': job_id,
        'username': user['username'],
        'archive_path': archive_path
        }
    application.q_out.publish_message(message)
    return job_id

#------------------------------------------------------------------------------

def handle_job_event(msg, listeners):
    LOGGER.info('Handle job event: {}'.format(msg))
    try:
        data = json.loads(msg)
        for listener in listeners:
            #if listener.username == data['username']:
            ret_msg = ['job-status', data['status']]
            listener.write_message(json.dumps(ret_msg))
    except Exception as e:
        LOGGER.error(e)
