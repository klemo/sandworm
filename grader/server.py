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

#------------------------------------------------------------------------------

define('env', default='local', help='running env (settings.ENV)', type=str)

#------------------------------------------------------------------------------

class Application(tornado.web.Application):

    def __init__(self, options):
        handlers = [
            (r'/', MainHandler),
            (r'/api/v1/labs$', LabHandler),
            (r'/api/v1/labs/(.+)', LabHandler),
            # (r'/login', LoginHandler),
            # (r'/logout', LogoutHandler)
            ]
        env = dict(
            template_path=os.path.join(
                os.path.dirname(__file__), 'templates'),
            static_path=os.path.join(
                os.path.dirname(__file__), 'static'),
            debug=settings.ENV['debug'],
            cookie_secret=settings.COOKIE_SECRET,
            xsrf_cookies=True,
            login_url='/login')
        #self.mongo = utils.connect_to_mongo(settings.ENV)
        tornado.web.Application.__init__(self, handlers, **env)

#------------------------------------------------------------------------------

class BaseHandler(tornado.web.RequestHandler):

    def get_current_user(self):
        return self.get_secure_cookie('password')

#------------------------------------------------------------------------------
    
class LoginHandler(BaseHandler):

    def get(self):
        self.render('login.html')

    def post(self):
        pswd = self.get_argument('password', '')
        if pswd == 'metatest':
            self.set_secure_cookie('password', 'true')
            self.redirect('/')
        else:
            self.redirect('/login')

#------------------------------------------------------------------------------
        
class LogoutHandler(BaseHandler):

    def get(self):
        self.clear_cookie('password')
        self.redirect('/')

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
