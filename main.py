import json
import logging
import os
import ssl
import sys
from tornado.auth import FacebookGraphMixin
from tornado.escape import json_decode, json_encode, url_escape
from tornado.gen import coroutine
from tornado.httpclient import AsyncHTTPClient
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options, parse_command_line
from tornado.web import Application, authenticated, RequestHandler, RedirectHandler, url, asynchronous, HTTPError, UIModule

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

class BaseHandler(RequestHandler):
    def get_current_user(self):
        user_json = self.get_secure_cookie("fbdemo_user")
        if not user_json:
            return None
        return json_decode(user_json)

class MainHandler(RequestHandler):
    @asynchronous
    @authenticated
    def get(self):
        https = AsyncHTTPClient()
        https.fetch("https://data.cityofnewyork.us/api/views/kku6-nxdu/rows.json?accessType=DOWNLOAD", callback=self.on_response)

    def on_response(self, response):
        if response.error:
            raise HTTPError(500)
        json = json_decode(response.body)
        self.write(json["meta"]["view"])
        self.finish()

class WebApp(Application):
    def __init__(self):
        """Responsible for global configuration, including the routing table that maps requests to handlers"""

        # How Tornado performs mappings between URLs and handlers
        handlers = [
            (r"/", MainHandler),
            url(r"/app", RedirectHandler, {"url": "https://www.imdb.com/title/tt0102685/"}),
            (r"/auth/login", AuthLoginHandler),
            (r"/auth/logout", AuthLogoutHandler)
        ]

        # Tornado settings
        settings = {
            "autoescape": None,
            "cookie_secret": "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            "debug": True,
            "facebook_api_key": options.facebook_api_key,
            "facebook_secret": options.facebook_secret,
            "login_url": "/auth/login",
            "static_path": os.path.join(os.path.dirname(__file__), "static"),
            "template_path": os.path.join(os.path.dirname(__file__), "templates"),
            "xsrf_cookies": True,
            "ui_modules": {"Post": PostModule}
        }

        # Used for single inheritance to call parent class
        super().__init__(handlers, **settings)

class AuthLoginHandler(BaseHandler, FacebookGraphMixin):
    @coroutine
    def get(self):
        if self.get_argument("code", False):
            user = yield self.get_authenticated_user(
                redirect_uri='https://localhost/',
                client_id=self.settings["facebook_api_key"],
                client_secret=self.settings["facebook_secret"],
                code=self.get_argument("code"))
        # Save the user with e.g. set_secure_cookie
        else:
            yield self.authorize_redirect(
                redirect_uri='https://localhost/',
                client_id=self.settings["facebook_api_key"])
                # extra_params={"scope": "read_stream,offline_access"})
                # code=self.get_argument("code"))

class AuthLogoutHandler(BaseHandler, FacebookGraphMixin):
    def get(self):
        self.clear_cookie("fbdemo_user")
        self.redirect(self.get_argument("next", "/"))

class PostModule(UIModule):
    def render(self, post):
        return self.render_string("modules/post.html", post=post)

def main():
    parse_command_line()
    if not (options.facebook_api_key and options.facebook_secret):
        print("--facebook_api_key and --facebook_secret must be set")
        return
    ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_ctx.load_cert_chain(os.path.join("./server", "server.pem"), os.path.join("./server", "server-key.pem"))
    http_server = HTTPServer(WebApp(), ssl_options=ssl_ctx)
    http_server.listen(options.port)
    IOLoop.current().start()

if __name__ == "__main__":
    main()
