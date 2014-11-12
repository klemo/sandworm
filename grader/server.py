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

#------------------------------------------------------------------------------

define('env', default='local', help='running env (settings.ENV)', type=str)

#------------------------------------------------------------------------------

class Application(tornado.web.Application):

    def __init__(self, options):
        handlers = [
            (r'/', MainHandler),
            (r'/api/v1/labs$', LabHandler),
            (r'/api/v1/labs/(.+)', LabHandler),
            (r'/login', LoginHandler),
            # (r'/logout', LogoutHandler)
            ]
        env = dict(
            template_path=os.path.join(
                os.path.dirname(__file__), 'templates'),
            static_path=os.path.join(
                os.path.dirname(__file__), 'static'),
            debug=settings.ENV['debug'],
            xsrf_cookies=False,
            login_url='/login')
        #self.mongo = utils.connect_to_mongo(settings.ENV)
        tornado.web.Application.__init__(self, handlers, **env)

#------------------------------------------------------------------------------

class BaseHandler(tornado.web.RequestHandler):

    def get_current_user(self):
        auth = utils.authenticate(self)
        if auth.get('error'):
            self.set_status(401)
        self.write(json.dumps(auth))

#------------------------------------------------------------------------------
    
class LoginHandler(BaseHandler):

    def post(self):
        user = json.loads(self.request.body)
        self.write(json.dumps(utils.login(user)))

#------------------------------------------------------------------------------
        
class LogoutHandler(BaseHandler):

    def get(self):
        self.redirect('/')

#------------------------------------------------------------------------------

class MainHandler(BaseHandler):

    def get(self):
        self.render('index.html')

    def post(self):
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
