from . import config
import app
import hashlib
from otpauth import OtpAuth
import web


class Login:
    def __init__(self):
        pass

    @staticmethod
    def GET(*a):
        message = None
        return config.render.login(message)

    @staticmethod
    def POST(*a):
        i = config.web.input()
        pwdhash = hashlib.md5(i.password + config.secret_key).hexdigest()
        check = config.model.validate_user(i.username, pwdhash)
        if check:
            app.session.loggedin = True
            app.session.username = check['username']
            app.session.privilege = check['privilege']
            change_pwd = check['change_pwd']
            tsa = check['two_step_authenticator']

            print "Force pwd: " + str(change_pwd)

            ip = web.ctx['ip']

            result = config.model_logs.insert_logs(check['username'], ip)
            print "login sessions: " + str(result)

            if check['status'] == 0:
                message = "User account disabled!!!!"
                return config.render.login(message)

            elif change_pwd == 1:
                print 'cambiar pwd'
                raise config.web.seeother('/users/change_pwd')
            elif tsa == 1:
                print 'tsa'
                app.session.loggedin = False
                raise config.web.seeother('/tsa')
            else:
                raise config.web.seeother('/')
        else:
            message = "User or Password are not correct!!!!"
            return config.render.login(message)
