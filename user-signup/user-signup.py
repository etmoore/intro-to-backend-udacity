import os
import jinja2
import webapp2

# configuration for jinja
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

class Handler(webapp2.RequestHandler):
    """Renders via jinja2 template engine"""
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class MainPage(Handler):
    def get(self):
        self.render("user_signup_form.html")

    def post(self):
        text = self.request.get("text")
        cipher = text.encode("rot13")
        self.render("user_signup_form.html", cipher = cipher)


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ], debug=True)
