import webapp2


form = """
<form method="post">
    What is your birthday?

    <br>
    <input type="text" name="month" placeholder="month">
    <input type="text" name="day" placeholder="day">
    <input type="text" name="year" placeholder="year">

    <br>
    <br>
    <input type="submit">
</form>
"""

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write(form)

    def post(self):
        self.response.write("Thanks! That's a totally valid day!")

app = webapp2.WSGIApplication([ ('/', MainPage), ], debug=True)
