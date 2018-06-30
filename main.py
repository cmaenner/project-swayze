import json
import logging
import os
import sys
import tornado.escape
from tornado.httpclient import AsyncHTTPClient
from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler, RedirectHandler, url, asynchronous, HTTPError

# Logging variables
logLevel = logging.DEBUG
logFileFormatter = "%(asctime)s %(levelname)s %(message)s"

# Enable Logging
try:
    logging.basicConfig(format=logFileFormatter, datefmt='%m/%d/%Y %I:%M:%S %p', level=logLevel)
    logging.getLogger(__name__)
except:
    sys.exit(1)

class MainHandler(RequestHandler):
    @asynchronous
    def get(self):
        https = AsyncHTTPClient()
        https.fetch("https://data.cityofnewyork.us/api/views/kku6-nxdu/rows.json?accessType=DOWNLOAD", callback=self.on_response)

    def on_response(self, response):
        if response.error:
            raise HTTPError(500)
        json = tornado.escape.json_decode(response.body)
        self.write(json["meta"]["view"])
        self.finish()

class WebApp(Application):
    def __init__(self):
        """Responsible for global configuration, including the routing table that maps requests to handlers"""

        # How Tornado performs mappings between URLs and handlers
        handlers = [
            (r"/", MainHandler),
            url(r"/app", RedirectHandler, {"url": "https://www.imdb.com/title/tt0102685/"})
        ]

        # Tornado settings
        settings = {
            "debug": True,
            "xsrf_cookies": True
        }
        # Used for single inheritance to call parent class
        super().__init__(handlers, **settings)

def main():
    WebApp().listen(8888)
    IOLoop.current().start()

if __name__ == "__main__":
    main()
