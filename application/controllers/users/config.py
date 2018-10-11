"""
    File for config the tables models and use HMAC
"""
import web
import hmac
import qrcode
from otpauth import OtpAuth
import application.models.model_users

render = web.template.render('application/views/users/', base='master')
model = application.models.model_users

secret_key = "kuorra_key"


def hash_str(s):
    return hmac.new(secret_key, s).hexdigest()


def make_secure_val(s):
    return "%s!%s" % (s, hash_str(s))


def check_secure_val(h):
    val = h.split('!')[0]
    if h == make_secure_val(val):
        return val

def create_tsa(username, user_hash):
    print str(user_hash)
    auth = OtpAuth(str(user_hash))  # a secret string
    s = auth.to_uri('totp', 'User:'+ username, 'Kuorra')
    img = qrcode.make(s)
    f = open("static/qr/output.png", "wb")
    img.save(f)
    f.close()
    