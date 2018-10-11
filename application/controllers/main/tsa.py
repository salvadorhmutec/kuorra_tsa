"""
    Class for change the password
"""
import application.controllers.main.config
import hashlib
from otpauth import OtpAuth
import app


class Tsa:
    def __init__(self):
        pass

    def GET(self, **k):
        #if app.session.loggedin is True: # validate if the user is logged
        if app.session.username != 'anonymous': # validate if the user is logged
            session_username = app.session.username # get the session_username
            session_privilege = app.session.privilege # get the session_privilege
            if session_privilege == 0: # admin user
                return self.GET_TSA(session_username) # call GET_TSA() function
            elif session_privilege == 1: # guess user
                return self.GET_TSA(session_username) # call GET_TSA() function
        else: # the user is not logged
            raise config.web.seeother('/login') # render login.html

    def POST(self, **k):
        #if app.session.loggedin is True: # validate if the user is logged
        if app.session.username != 'anonymous': # validate if the user is logged
            session_username = app.session.username # get the session_username
            session_privilege = app.session.privilege # get the session_privilege
            if session_privilege == 0: # admin user
                return self.POST_TSA(session_username) # call POST_TSA() function
            elif session_privilege == 1: # guess user
                return self.POST_TSA(session_username)# call POST_TSA() function
        else: # the user is not logged
            raise config.web.seeother('/login') # render login.html

    @staticmethod
    def GET_TSA(username, **k):
        message = None # Error message
        result = config.model.get_users(username) # search for username data
        print result
        result.username = config.make_secure_val(str(result.username)) # apply HMAC for username
        return config.render.tsa(result, message) # render tsa.html

    @staticmethod
    def POST_TSA(username, **k):
        message = None # Error message
        form = config.web.input() # get form data
        result = config.model.get_users(username) # search for username data
        user_hash = str(result.user_hash)
        
        auth = OtpAuth(user_hash)
        if auth.valid_totp(form.authenticator):
            app.session.loggedin = True
            raise config.web.seeother('/')
        else:
            message = "Two Step Authenticator not valid" # Error message
            result = config.model.get_users(username) # search for username data
            result.username = config.make_secure_val(str(result.username)) # apply HMAC for username
            return config.render.tsa(result, message) # render tsa.html
