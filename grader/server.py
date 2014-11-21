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
import tornado.auth
import tornado.escape
from tornado.options import define, options
# application imports
import os.path
import pymongo
import simplejson as json
import urllib
import settings
import utils
import db
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
        
#------------------------------------------------------------------------------
        
if __name__ == '__main__':
    tornado.options.parse_command_line()
    settings.ENV = settings.SERVER[options.env]
    http_server = tornado.httpserver.HTTPServer(Application(options))
    http_server.listen(settings.ENV['port'])
    tornado.ioloop.IOLoop.instance().start()
