import os
import re
import random
import hashlib
import hmac
from string import letters

import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

secret = 'opie'

def make_secure_val(val):
    return '%s|%s' % (val, hmac.new(secret, val).hexdigest())

def check_secure_val(secure_val):
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val

#### USER STUFF ####

def make_salt(length = 5):
    return ''.join(random.choice(letters) for x in range(length))

def make_pw_hash(name, pw, salt = None):
    salt = salt or make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)

def valid_username(username):
    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    return USER_RE.match(username)

def valid_password(password):
    PASSWORD_RE = re.compile(r"^.{3,20}$")
    return PASSWORD_RE.match(password)

def valid_email(email):
    EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
    return not email or EMAIL_RE.match(email)

class User(db.Model):
    name = db.StringProperty(required = True)
    pw_hash = db.StringProperty(required = True)
    email = db.StringProperty()

    @classmethod
    def register(cls, name, pw, email=None):
        pw_hash = make_pw_hash(name, pw)
        return User(name = name,
                pw_hash = pw_hash,
                email = email)

        #### BLOG STUFF ####
class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def set_secure_cookie(self, name, val):
        cookie_val = make_secure_val(val)
        self.response.headers.add_header(
                'Set-Cookie',
                '%s=%s; Path=/' % (name, cookie_val))

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        if cookie_val:
            return check_secure_val(cookie_val)

    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))

class SignupPage(Handler):
    def get(self):
        self.render("user-signup-form.html")

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        if (valid_username(username) and
            valid_password(password) and
            password == verify and
            valid_email(email)):

            u = User.all().filter('name =', username).get()
            if u:
                error = { "username": "That user already exists." }
                self.render('user-signup-form.html',
                            error=error,
                            username=username,
                            email=email)

            else:
                u = User.register(username, password, email)
                u.put()

                self.login(u)
                self.redirect('/welcome')

        else:
            error = {}
            if not valid_username(username):
                error["username"] = "That's not a valid username"
            if not valid_password(password):
                error["password"] = "That's not a valid password"
            if not password == verify:
                error["verify"] = "Your passwords didn't match"
            if not valid_email(email):
                error["email"] = "That's not a valid email"

            self.render("user-signup-form.html",
                        username=username,
                        email=email,
                        error=error)


class WelcomePage(Handler):
    def get(self):
        uid = self.read_secure_cookie('user_id')
        if uid:
            user = User.get_by_id(int(uid))
        if user:
            self.render('welcome.html', username = user.name)
        else:
            self.redirect('/signup')


app = webapp2.WSGIApplication([('/signup', SignupPage),
                               ('/welcome', WelcomePage)],
                               debug=True)
