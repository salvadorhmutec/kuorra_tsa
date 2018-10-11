"""
    Class for change password
"""
import application.controllers.users.config as config
import hashlib
import app


class Atsa:
    def __init__(self):
        pass

    def GET(self, **k):
        if app.session.loggedin is True: # validate if the user is logged
            session_username = app.session.username # get the session_username
            session_privilege = app.session.privilege # get the session_privilege
            print "atsa: " + session_username
            if session_privilege == 0: # admin user
                return self.GET_ATSA(session_username) # call GET_CHANGE_PWD() function
            elif session_privilege == 1: # guess user
                return self.GET_ATSA(session_username) # call GET_CHANGE_PWD() function
        else: # the user is not logged
            raise config.web.seeother('/login') # render login.html

    def POST(self, **k):
        if app.session.loggedin is True: # validate if the user is logged
            session_username = app.session.username # get the session_username
            session_privilege = app.session.privilege # get the session_privilege
            if session_privilege == 0: # admin user
                return self.POST_ATSA(session_username) # call POST_CHANGE_PWD() function
            elif session_privilege == 1: # guess user
                return self.POST_ATSA(session_username)# call POST_CHANGE_PWD() function
        else: # the user is not logged
            raise config.web.seeother('/login') # render login.html

    @staticmethod
    def GET_ATSA(username, **k):
        message = None # Error message
        result = config.model.get_users(username) # search for username data
        user_hash = str(result.user_hash)
        print user_hash
        config.create_tsa(username, user_hash)
        result.username = config.make_secure_val(str(result.username)) # apply HMAC for username
        return config.render.atsa(result, message) # render chage_pwd.html

    @staticmethod
    def POST_ATSA(username, **k):
        message = None # Error message
        form = config.web.input() # get form data
        
        result = config.model.update_two_step_authenticator(
                username,
                form['two_step_authenticator']
            )
        if result == None:
            message = "Error on two step authenticator" # Error message
            result = config.model.get_users(username) # search for username data
            result.username = config.make_secure_val(str(result.username)) # apply HMAC for username
            return config.render.atsa(result, message) # render chage_pwd.html
        else:
            raise config.web.seeother('/users')
