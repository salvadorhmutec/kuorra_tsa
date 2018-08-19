import web
import qrcode
import hmac
import application.models.model_users
import application.models.model_logs

render = web.template.render('application/views/main/', base='master')
model = application.models.model_users
model_logs = application.models.model_logs

secret_key = "kuorra_key"

def reset_qr():
    img = qrcode.make('kuorra')
    f = open("static/qr/output.png", "wb")
    img.save(f)
    f.close()

def hash_str(s):
    return hmac.new(secret_key, s).hexdigest()


def make_secure_val(s):
    return "%s!%s" % (s, hash_str(s))


def check_secure_val(h):
    val = h.split('!')[0]
    if h == make_secure_val(val):
        return val