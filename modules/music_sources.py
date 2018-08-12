#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

# Modules
from tornado.escape import json_decode
from tornado.httpclient import AsyncHTTPClient
from tornado.ioloop import IOLoop
from tornado.web import asynchronous, authenticated, HTTPError

# Application modules
from modules.tornado_application import BaseHandler

class Soundcloud(BaseHandler):
    """Get Soundcloud resources and normalize data"""

    # @authenticated
    @asynchronous
    async def get(self):
        """HTTP GET Method"""

        # An non-blocking HTTP client
        await AsyncHTTPClient().fetch("https://soundcloud.com/tomberlinmusic/tracks", callback=self.onResponse)

    def onResponse(self, response):
        """Respond with a JSON response"""

        # Exception on HTTP error
        if response.error:
            raise HTTPError(500)

        # Get body and decode into JSON
        json = json_decode(response.body)

        # Writes the given chunk to the output buffer
        self.write(json["meta"]["view"])

        # Finishes this response, ending the HTTP request
        self.finish()
