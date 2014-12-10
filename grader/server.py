#------------------------------------------------------------------------------
# -*- coding: utf-8 -*-
# server.py
# description: tornado web server core file
#------------------------------------------------------------------------------

# tornado imports
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import tornado.auth
import tornado.escape
from tornado.options import define, options
# application imports
import sockjs.tornado
import os.path
import pymongo
import uuid
import simplejson as json
import logging
import settings
import utils
import db
import mq
import creds

#------------------------------------------------------------------------------

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)

#------------------------------------------------------------------------------

define('env', default='local', help='running env (settings.ENV)', type=str)

#------------------------------------------------------------------------------

class Application(tornado.web.Application):

    def __init__(self, options):
        handlers = [
            # Public API
            (r'/', MainHandler),
            (r'/api/v1/login', LoginHandler),
            (r'/api/v1/logout', LogoutHandler),
            (r'/api/v1/user', UserHandler),
            # User API
            (r'/api/v1/labs$', LabHandler),
            (r'/api/v1/labs/(.+)', LabHandler),
            # Admin API
            (r'/api/v1/admin/labs$', AdminLabHandler),
            (r'/api/v1/admin/labs/(.+)', AdminLabHandler),
            (r'/api/v1/admin/results', AdminResultsHandler),
            ] + sockjs.tornado.SockJSRouter(SubmitLabHandler,
                                            '/api/v1/submitjob').urls
        env = dict(
            template_path=os.path.join(
                os.path.dirname(__file__), 'templates'),
            static_path=os.path.join(
                os.path.dirname(__file__), 'static'),
            debug=settings.ENV['debug'],
            xsrf_cookies=True,
            cookie_secret=creds.COOKIE_SECRET)
        self.db = utils.connect_to_mongo(settings.ENV)
        tornado.web.Application.__init__(self, handlers, **env)

#------------------------------------------------------------------------------

class BaseHandler(tornado.web.RequestHandler):

    def get_current_user(self):
        username = self.get_secure_cookie('username')
        return db.get_user(self.application.db, username)

#------------------------------------------------------------------------------
# Public API
#------------------------------------------------------------------------------
    
class LoginHandler(BaseHandler):

    def post(self):
        logindata = json.loads(self.request.body)
        user, err = db.login_user(self.application.db, logindata)
        if user:
            self.set_secure_cookie('username', user['username'])
            utils.jsonify(self, user)
        else:
            self.set_status(401)
            utils.jsonify(self, {'code': 'login-failed', 'err': err})

#------------------------------------------------------------------------------

class LogoutHandler(BaseHandler):

    @utils.auth()
    def get(self):
        self.clear_cookie('username')
        utils.jsonify(self, True)

#------------------------------------------------------------------------------

class MainHandler(BaseHandler):

    def get(self):
        self.xsrf_token
        self.render('index.html')

#------------------------------------------------------------------------------

class UserHandler(BaseHandler):

    @utils.auth()
    def get(self):
        utils.jsonify(self, self.get_current_user())

#------------------------------------------------------------------------------
# Admin API
#------------------------------------------------------------------------------
        
class AdminLabHandler(BaseHandler):

    @utils.auth('admin')
    def get(self, lab_id=None):
        utils.jsonify(self, db.get_admin_labs(self.application.db, lab_id))

    @utils.auth('admin')
    def post(self, lab_id=None):
        postdata = json.loads(self.request.body)
        lab, err = db.save_admin_lab(self.application.db, postdata)
        if lab:
            utils.jsonify(self, lab)
        else:
            self.set_status(400)
            utils.jsonify(self, {'code': 'save-failed', 'err': err})

    @utils.auth('admin')
    def delete(self, lab_id=None):
        try:
            db.delete_admin_lab(self.application.db, lab_id)
            utils.jsonify(self, True)
        except Exception as e:
            LOGGER.error(e)
            self.set_status(400)
            utils.jsonify(self, {'code': 'delete-failed', 'err': ''})

#------------------------------------------------------------------------------

class AdminResultsHandler(BaseHandler):

    @utils.auth('admin')
    def get(self):
        utils.jsonify(self, db.get_admin_all_results(self.application.db))

#------------------------------------------------------------------------------
# User API
#------------------------------------------------------------------------------
        
class LabHandler(BaseHandler):

    @utils.auth('user')
    def get(self, lab_id=None):
        utils.jsonify(self, db.get_labs(self.application.db,
                                        self.get_current_user(),
                                        lab_id))

    @utils.auth('user')
    def post(self):
        user = self.get_current_user()
        try:
            archive_path = db.save_uploaded_archive(self.request, user)
            db.submit_job(self.application, archive_path, user)
            utils.jsonify(self, True)
        except Exception as e:
            LOGGER.error(e)
            utils.jsonify(self, {'code': 'upload failed'})

#------------------------------------------------------------------------------
        
class SubmitLabHandler(sockjs.tornado.SockJSConnection):
    '''
    Handles real-time async bidirectional connection for submitting labs for
    remote execution using EXEC system
    '''

    # TODO this will probaby end up in Redis...
    users = set()

    def on_open(self, *args):
        print('SockJS connection opened')
        self.users.add(self)

    def on_message(self, message):
        print 'Received WS message: ', message
        print 'Sending WS message: ', message
        self.send(message)
        
    def on_close(self):
        self.users.remove(self)
        print('SockJS connection closed')

#------------------------------------------------------------------------------
        
if __name__ == '__main__':
    tornado.options.parse_command_line()
    settings.ENV = settings.SERVER[options.env]
    application = Application(options)
    http_server = tornado.httpserver.HTTPServer(application)
    io_loop = tornado.ioloop.IOLoop.instance()    
    application.q = mq.QConsumer(settings.QUEUE_IN)
    application.q_out = mq.QProducer(settings.QUEUE_OUT)
    http_server.listen(settings.ENV['port'])
    io_loop.start()
