import logging
import sys
import tornado.ioloop
from tornado.web import Application, RequestHandler, url

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
    def get(self):
        self.write("Hello, world")

class BaseHandler(RequestHandler):
    def initialize(self, base):
        self.base = base

def app():
    return Application([
        (r"/", MainHandler),
    ], debug=True, xsrf_cookies=True)

def main():
    app().listen(8888)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
