#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

# Modules
from tornado.escape import json_decode
from tornado.httpclient import AsyncHTTPClient
from tornado.ioloop import IOLoop
from tornado.web import asynchronous, authenticated, HTTPError

# Application modules
from modules.tornado_authentication import BaseHandler

class MainHandler(BaseHandler):
    """Class used to handle root HTTP requests"""

    @authenticated
    @asynchronous
    async def get(self):
        https = AsyncHTTPClient()
        await https.fetch("https://data.cityofnewyork.us/api/views/kku6-nxdu/rows.json?accessType=DOWNLOAD", callback=self.on_response)

    def on_response(self, response):
        if response.error:
            raise HTTPError(500)
        json = json_decode(response.body)
        self.write(json["meta"]["view"])
        self.finish()
