import webapp2


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

class MainPage(webapp2.RequestHandler):
    def write_form(self, error=""):
        values = {'month': self.request.get('month'),
                  'day': self.request.get('day'),
                  'year': self.request.get('year'),
                  'error': error}
        self.response.out.write(form % values)

    def get(self):
        self.write_form()

    def post(self):
        user_month = valid_month(self.request.get('month'))
        user_day = valid_day(self.request.get('day'))
        user_year = valid_year(self.request.get('year'))

        if not (user_month and user_day and user_year):
            self.write_form("That doesn't look right to me, friend.")
        else:
            self.response.out.write("Thanks! That's a totally valid day!")


app = webapp2.WSGIApplication([ ('/', MainPage), ], debug=True)
