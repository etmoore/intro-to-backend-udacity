import os
import re
import jinja2
import webapp2

# configuration for jinja
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return USER_RE.match(username)

PASSWORD_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return PASSWORD_RE.match(password)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
    return EMAIL_RE.match(email)

class Handler(webapp2.RequestHandler):
    """Renders via jinja2 template engine"""
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class SignupPage(Handler):
    def get(self):
        self.render("user_signup_form.html")

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        if (valid_username(username) and
                valid_password(password) and
                password == verify and
                valid_email(email)):
            self.redirect("/welcome?username=" + username)

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

            self.render("user_signup_form.html",
                        username = username,
                        email = email,
                        error = error)

class WelcomePage(Handler):
    def get(self):
        self.render("welcome.html",
                    username = self.request.get("username"))

app = webapp2.WSGIApplication([
    ('/', SignupPage),
    ('/welcome', WelcomePage),
    ], debug=True)
