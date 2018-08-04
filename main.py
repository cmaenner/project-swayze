#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Chris Maenner"
__copyright__ = "Copyright 2018, The Swayze Project"
__credits__ = ["Chris Maenner"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Chris Maenner"
__email__ = "christopher@dafinga.net"
__status__ = "Development"

import base64
import json
import graphene
import logging
import os
import ssl
import sys
import os.path
import tornado.auth
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
from modules.tornado_graphql_handler import TornadoGraphQLHandler
from modules.tornado_authentication import BaseHandler, AuthLoginHandler, AuthLogoutHandler
from modules.schema import schema
from modules.tornado_graphql_handler import TornadoGraphQLHandler

# Default CLI parameters
define("port", default=443, help="run on the given port", type=int)
define("facebook_api_key", help="your Facebook application API key", type=str)
define("facebook_secret", help="your Facebook application secret", type=str)

# Logging variables
logLevel = logging.DEBUG
logFileFormatter = "%(asctime)s %(levelname)s %(message)s"

# Enable Logging
try:
    logging.basicConfig(format=logFileFormatter, datefmt='%m/%d/%Y %I:%M:%S %p', level=logLevel)
    logging.getLogger(__name__)
except:
    sys.exit(1)

class Application(tornado.web.Application):
    def __init__(self):
        """Responsible for global configuration, including the routing table that maps requests to handlers"""

        # How Tornado performs mappings between URLs and handlers
        handlers = [
            (r"/", MainHandler),
            tornado.web.url(r"/app", tornado.web.RedirectHandler, {"url": "https://www.imdb.com/title/tt0102685/"}),
            (r"/auth/login", AuthLoginHandler),
            (r"/auth/logout", AuthLogoutHandler),
            (r"/graphql", TornadoGraphQLHandler, dict(graphiql=False, schema=schema))
        ]

        # Tornado settings
        settings = {
            "cookie_secret": "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            "login_url": "/auth/login",
            "template_path": os.path.join(os.path.dirname(__file__), "templates"),
            "static_path": os.path.join(os.path.dirname(__file__), "static"),
            "xsrf_cookies": True,
            "facebook_api_key": options.facebook_api_key,
            "facebook_secret": options.facebook_secret,
            "ui_modules": {"Post": PostModule},
            "dubug": True,
            "autoescape": None
        }

        # Used for single inheritance to call parent class
        tornado.web.Application.__init__(self, handlers, **settings)

class MainHandler(BaseHandler, tornado.auth.FacebookGraphMixin):
    @tornado.web.authenticated
    @tornado.web.asynchronous
    async def get(self):
        https = tornado.httpclient.AsyncHTTPClient()
        await https.fetch("https://data.cityofnewyork.us/api/views/kku6-nxdu/rows.json?accessType=DOWNLOAD", callback=self.on_response)

    def on_response(self, response):
        if response.error:
            raise tornado.web.HTTPError(500)
        json = tornado.escape.json_decode(response.body)
        self.write(json["meta"]["view"])
        self.finish()

class PostModule(tornado.web.UIModule):
    def render(self, post):
        return self.render_string("modules/post.html", post=post)

def main():
    tornado.options.parse_command_line()
    if not (options.facebook_api_key and options.facebook_secret):
        logging.info("--facebook_api_key and --facebook_secret must be set")
        return
    ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_ctx.load_cert_chain(os.path.join("./server", "server.pem"), os.path.join("./server", "server-key.pem"))
    http_server = tornado.httpserver.HTTPServer(Application(), ssl_options=ssl_ctx)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
