#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

from tornado.auth import FacebookGraphMixin
from tornado.escape import json_decode, json_encode, url_escape
from tornado.web import RequestHandler, UIModule

class BaseHandler(RequestHandler):
    def get_current_user(self):
        user_json = self.get_secure_cookie("user")
        if not user_json:
            return None
        return json_decode(user_json)

class AuthLoginHandler(BaseHandler, FacebookGraphMixin):
    async def get(self):
        my_url = (self.request.protocol + "://" + self.request.host +
                  "/auth/login?next=" +
                  url_escape(self.get_argument("next", "/")))
        if self.get_argument("code", False):
            user = await self.get_authenticated_user(
                redirect_uri=my_url,
                client_id=self.settings["facebook_api_key"],
                client_secret=self.settings["facebook_secret"],
                code=self.get_argument("code"))

            self.set_secure_cookie("user", json_encode(user))
            self.redirect(self.get_argument("next", "/"))
            return
        self.authorize_redirect(
            redirect_uri=my_url,
            client_id=self.settings["facebook_api_key"],
            extra_params={"scope": "user_posts"}
        )

class AuthLogoutHandler(BaseHandler, FacebookGraphMixin):
    def get(self):
        # self.clear_cookie("fbdemo_user")
        self.clear_cookie("user")
        self.redirect(self.get_argument("next", "/"))

class PostModule(UIModule):
    def render(self, post):
        return self.render_string("fb_post.html", post=post)
