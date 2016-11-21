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
    body = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True,
                                  required = True)

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
        posts = db.GqlQuery("Select * from Post "
                           "ORDER BY created DESC ")
        self.render("posts.html", posts=posts)

class New(Handler):
    def get(self):
        self.render("new_post.html")

    def post(self):
        title = self.request.get('subject')
        body = self.request.get('content')
        if title and body:
            p = Post(title=title, body=body)
            p.put()

            permalink = "/%s" % p.key().id()
            self.redirect(permalink)
        else:
            error = "Posts must have a title and body!"
            self.render("new_post.html", error=error,
                        title=title, body=body)


class Show(Handler):
    def get(self, post_id):
        post_id = int(post_id)
        post = Post.get_by_id(post_id)
        self.render("post.html", post=post)

app = webapp2.WSGIApplication([
    ('/', Index),
    ('/newpost', New),
    ('/(\d+)', Show),
    ], debug=True)
