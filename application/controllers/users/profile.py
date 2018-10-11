"""
    Class for show a user detail
"""
import application.controllers.users.config as config
import app
import qrcode
from otpauth import OtpAuth


class Profile:
    def __init__(self):
        pass

    def GET(self, **k):
        if app.session.loggedin is True:  # validate if the user is logged
            session_username = app.session.username
            session_privilege = app.session.privilege  # get the session_privilege
            session_username = config.make_secure_val(session_username)
            if session_privilege == 0:  # admin user
                return self.GET_PROFILE(session_username)  # call GET_VIEW() function
            elif session_privilege == 1:  # guess user
                return self.GET_PROFILE(session_username)  # call GET_VIEW() function
                #raise config.web.seeother('/')  # render guess.html
        else:  # the user dont have logged
            raise config.web.seeother('/login')  # render login.html

    @staticmethod
    def GET_PROFILE(username):
        username = config.check_secure_val(str(username))  # HMAC username validate
        result = config.model.get_users(username)  # search for the user data
        user_hash = str(result.user_hash)
        print user_hash
        config.create_tsa(username, user_hash)
        return config.render.profile(result)  # render view.html with user data
