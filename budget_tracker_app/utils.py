from calendar import HTMLCalendar
from django.shortcuts import redirect

from .helper import get_current_user
from .models import ExpenseInfo


class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    # formats a day as a td
    # filter events by day
    def formatday(self, day, expenses):
        expenses_per_day = expenses.filter(date_added__day=day)
        d = ''

        for expense in expenses_per_day:
            d += f'<li> {expense.get_html_url} </li>'

        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        return '<td></td>'

    # formats a week as a tr
    def formatweek(self, theweek, expenses, **kwargs):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, expenses)
        return f'<tr> {week} </tr>'

    # formats a month as a table
    # filter events by year and month
    def formatmonth(self, withyear=True, **kwargs):
        expenses = ExpenseInfo.objects.filter(date_added__year=self.year, date_added__month=self.month,
                                              user_expense=get_current_user())

        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, expenses)}\n'
        return cal


def anonymous_required(redirect_url, **kwargs):
    """
    Decorator for views that allow only unauthenticated users to access view.
    Usage:
    @anonymous_required(redirect_url='company_info')
    def homepage(request):
        return render(request, 'homepage.html')
    """

    def _wrapped(view_func, *args, **kwargs):
        def check_anonymous(request, *args, **kwargs):
            view = view_func(request, *args, **kwargs)
            if request.user.is_authenticated():
                return redirect(redirect_url)
            return view

        return check_anonymous

    return _wrapped
