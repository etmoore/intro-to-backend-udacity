import os
import jinja2
import webapp2

from google.appengine.ext import db

# configuration for jinja
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

class Post(db.Model):
    title = db.StringProperty(required = True)
    post = db.TextProperty(required = True)
    created = db.DateTimeProperty(required = True)

class Handler(webapp2.RequestHandler):
    """Renders via jinja2 template engine"""
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class Index(Handler):
    def get(self):
        self.write("posts!")

class New(Handler):
    def get(self):
        self.write("new post!")

class Show(Handler):
    def get(self, post_id):
        self.write("single post!")

app = webapp2.WSGIApplication([
    ('/', Index),
    ('/newpost', New),
    ('/(\d+)', Show),
    ], debug=True)
