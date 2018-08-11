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

import json
import logging
import os.path
import ssl
import sys
from tornado.auth import FacebookGraphMixin
from tornado.escape import json_decode
from tornado.httpclient import AsyncHTTPClient
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application, asynchronous, authenticated, HTTPError, RedirectHandler, UIModule, url
from tornado.options import define, options, parse_command_line, parse_config_file

# Application modules
from modules.music_sources import Soundcloud
from modules.tornado_application import BaseHandler, AuthLoginHandler, AuthLogoutHandler, PostModule
from modules.tornado_graphql_handler import TornadoGraphQLHandler
from modules.tornado_main import MainHandler
from modules.schema import schema

# Default CLI parameters
define("port", default=443, help="run on the given port", type=int)
define("facebook_api_key", help="your Facebook application API key", type=str)
define("facebook_secret", help="your Facebook application secret", type=str)

# # Logging variables
# logLevel = logging.DEBUG
# logFileFormatter = "%(asctime)s %(levelname)s %(message)s"

# # Enable Logging
# try:
#     logging.basicConfig(format=logFileFormatter, datefmt='%m/%d/%Y %I:%M:%S %p', level=logLevel)
#     logging.getLogger(__name__)
# except:
#     sys.exit(1)

class Swayze(Application):
    def __init__(self):
        """Responsible for global configuration, including the routing table that maps requests to handlers"""

        # How Tornado performs mappings between URLs and handlers
        handlers = [
            (r"/", MainHandler),
            url(r"/app", RedirectHandler, {"url": "https://www.imdb.com/title/tt0102685/"}),
            (r"/auth/login", AuthLoginHandler),
            (r"/auth/logout", AuthLogoutHandler),
            (r"/graphql", TornadoGraphQLHandler, dict(graphiql=False, schema=schema)),
            (r"/soundcloud", Soundcloud)
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
        Application.__init__(self, handlers, **settings)

def main():
    """Primary function to start application"""

    # Options to define application parameters
    parse_command_line()

    # Verify user inputted Facebook API key/secret
    if not (options.facebook_api_key and options.facebook_secret):
        logging.info("--facebook_api_key and --facebook_secret must be set")
        return

    # Enable SSL web server, needed for Facebook auth support
    sslCtx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    sslCtx.load_cert_chain(os.path.join("./server", "server.pem"), os.path.join("./server", "server-key.pem"))

    # Start web application
    httpServer = HTTPServer(Swayze(), ssl_options=sslCtx)
    httpServer.listen(options.port)

    # Start the I/O loop for the current thread
    IOLoop.current().start()

if __name__ == "__main__":
    main()
