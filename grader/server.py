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
import creds

#------------------------------------------------------------------------------

define('env', default='local', help='running env (settings.ENV)', type=str)

#------------------------------------------------------------------------------

class Application(tornado.web.Application):

    def __init__(self, options):
        handlers = [
            (r'/', MainHandler),
            (r'/api/v1/labs$', LabHandler),
            (r'/api/v1/labs/(.+)', LabHandler),
            (r'/api/v1/login', LoginHandler),
            (r'/api/v1/logout', LogoutHandler),
            (r'/api/v1/user', UserHandler)
            ]
        env = dict(
            template_path=os.path.join(
                os.path.dirname(__file__), 'templates'),
            static_path=os.path.join(
                os.path.dirname(__file__), 'static'),
            debug=settings.ENV['debug'],
            xsrf_cookies=True,
            cookie_secret=creds.COOKIE_SECRET,
            login_url='/')
        #self.mongo = utils.connect_to_mongo(settings.ENV)
        tornado.web.Application.__init__(self, handlers, **env)

#------------------------------------------------------------------------------

class BaseHandler(tornado.web.RequestHandler):

    def get_current_user(self):
        return self.get_secure_cookie('user')

#------------------------------------------------------------------------------
    
class LoginHandler(BaseHandler):

    def post(self):
        user = json.loads(self.request.body)
        # devel only, obviously...
        if user['password'] == 'test':
            self.set_secure_cookie('username', user['username'])
            self.write(json.dumps({'username': user['username']}))
        else:
            self.set_status(401)
            self.write(json.dumps({'msg': 'username/password error'}))

#------------------------------------------------------------------------------

class LogoutHandler(BaseHandler):

    def get(self):
        if self.get_secure_cookie('username'):
            self.clear_cookie('username')
            self.finish(json.dumps(True))
        else:
            self.finish(json.dumps(False))

#------------------------------------------------------------------------------

class UserHandler(BaseHandler):

    def get(self):
        username = self.get_secure_cookie('username')
        if username:
            self.finish(json.dumps({'username': username}))
        else:
            self.set_status(400)
            self.finish(json.dumps(False))

#------------------------------------------------------------------------------

class MainHandler(BaseHandler):

    def get(self):
        self.render('index.html')

#------------------------------------------------------------------------------

class LabHandler(BaseHandler):

    def get(self, lab_id=None):
        if lab_id:
            self.write(json.dumps(True))
        else:
            self.write(json.dumps([1,2,3]))
        
#------------------------------------------------------------------------------
        
if __name__ == '__main__':
    tornado.options.parse_command_line()
    settings.ENV = settings.SERVER[options.env]
    http_server = tornado.httpserver.HTTPServer(Application(options))
    http_server.listen(settings.ENV['port'])
    tornado.ioloop.IOLoop.instance().start()
