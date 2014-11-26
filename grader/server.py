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
import os.path
import uuid
import pymongo
import simplejson as json
import urllib
import settings
import utils
import db
import mq
import creds

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
            (r'/api/v1/submitlabstatus', SubmitLabHandler),
            # Admin API
            (r'/api/v1/admin/labs$', AdminLabHandler),
            (r'/api/v1/admin/labs/(.+)', AdminLabHandler),
            (r'/api/v1/admin/results', AdminResultsHandler),
            ]
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
            err = db.delete_admin_lab(self.application.db, lab_id)
            utils.jsonify(self, True)
        except Exception as e:
            self.set_status(400)
            utils.jsonify(self, {'code': 'delete-failed', 'err': e})    

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
        filepost = self.request.files.get('file')
        if not filepost:
            utils.jsonify(self, False)
        fileinfo = filepost[0]
        fname = fileinfo['filename']
        ext = os.path.splitext(fname)[1]
        name = str(uuid.uuid4()) + ext
        if not os.path.exists(settings.UPLOAD_DIR):
            os.makedirs(settings.UPLOAD_DIR)
        with open(os.path.join(settings.UPLOAD_DIR, name), 'wb') as f:
            f.write(fileinfo['body'])
        utils.jsonify(self, True)

#------------------------------------------------------------------------------

WSUSERS = []
        
class SubmitLabHandler(tornado.websocket.WebSocketHandler):

    def open(self, *args):
        print('open', 'WebSocketChatHandler', self)
        WSUSERS.append(self)

    def on_message(self, message):
        print message
        for client in WSUSERS:
            WSUSERS.write_message(message)
        
    def on_close(self):
        clients.remove(self)

#------------------------------------------------------------------------------
        
if __name__ == '__main__':
    tornado.options.parse_command_line()
    settings.ENV = settings.SERVER[options.env]
    application = Application(options)
    http_server = tornado.httpserver.HTTPServer(application)
    io_loop = tornado.ioloop.IOLoop.instance()    
    application.q = mq.PikaClient(settings.QUEUE)
    http_server.listen(settings.ENV['port'])
    io_loop.start()
