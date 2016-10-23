import webapp2
import cgi


form = """
<form method="post">
    What is your birthday?

    <br>
    <input type="text" name="month" placeholder="month" value="%(month)s">
    <input type="text" name="day" placeholder="day" value="%(day)s">
    <input type="text" name="year" placeholder="year" value="%(year)s">
    <div style="color: red">%(error)s</div>
    <br>
    <br>
    <input type="submit">
</form>
"""

def valid_month(month):
    if month:
        month = month.capitalize()
        months = ['January',
                'February',
                'March',
                'April',
                'May',
                'June',
                'July',
                'August',
                'September',
                'October',
                'November',
                'December']

        if month in months:
            return month

def valid_day(day):
    if day and day.isdigit():
        day = int(day)
        if day <= 31 and day > 0:
            return day

def valid_year(year):
    if year and year.isdigit():
        year = int(year)
        if year >= 1900 and year <= 2020:
            return year

def escape_html(s):
    return cgi.escape(s, quote = True)

class MainPage(webapp2.RequestHandler):
    def write_form(self, error="", month="", day="", year=""):
        self.response.out.write(form % {'error': error,
                                        'month': escape_html(month),
                                        'day': escape_html(day),
                                        'year': escape_html(year)})

    def get(self):
        self.write_form()

    def post(self):
        user_month = self.request.get('month')
        user_day = self.request.get('day')
        user_year = self.request.get('year')

        month = valid_month(user_month)
        day = valid_day(user_day)
        year = valid_year(user_year)

        if not (month and day and year):
            self.write_form("That doesn't look right to me, friend.",
                            user_month, user_day, user_year)
        else:
            self.redirect("/thanks");

class ThanksHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Thanks! That's a totally valid day!")

app = webapp2.WSGIApplication([ ('/', MainPage), ('/thanks', ThanksHandler)],
                              debug=True)
