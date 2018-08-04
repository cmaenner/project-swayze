import tornado

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        # user_json = self.get_secure_cookie("fbdemo_user")
        user_json = self.get_secure_cookie("user")
        if not user_json:
            return None
        return tornado.escape.json_decode(user_json)

class AuthLoginHandler(BaseHandler, tornado.auth.FacebookGraphMixin):
    async def get(self):
        my_url = (self.request.protocol + "://" + self.request.host +
                  "/auth/login?next=" +
                  tornado.escape.url_escape(self.get_argument("next", "/")))
        if self.get_argument("code", False):
            user = await self.get_authenticated_user(
                redirect_uri=my_url,
                client_id=self.settings["facebook_api_key"],
                client_secret=self.settings["facebook_secret"],
                code=self.get_argument("code"))

            self.set_secure_cookie("user", tornado.escape.json_encode(user))
            self.redirect(self.get_argument("next", "/"))
            return
        self.authorize_redirect(
            redirect_uri=my_url,
            client_id=self.settings["facebook_api_key"],
            extra_params={"scope": "user_posts"}
        )


class AuthLogoutHandler(BaseHandler, tornado.auth.FacebookGraphMixin):
    def get(self):
        # self.clear_cookie("fbdemo_user")
        self.clear_cookie("user")
        self.redirect(self.get_argument("next", "/"))
