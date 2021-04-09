import calendar
from datetime import datetime, date, timedelta

from django.views import generic
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from django.views.generic.base import View

from budget_tracker_app.forms import SignUpForm, LoginForm, ExpenseForm
from budget_tracker_app.models import ExpenseInfo
from budget_tracker_app.utils import Calendar

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


class WelcomeView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'budget_tracker_app/welcome.html')


class SignUpView(View):

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST or None)
        if form.is_valid():
            User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            user = authenticate(username=form.cleaned_data['username'], passsword=form.cleaned_data['password1'])
            return redirect('hello_world')
        context = {
            'form': form
        }
        return render(request, 'budget_tracker_app/signup.html', context)

    def get(self, request, *args, **kwargs):
        form = SignUpForm(request.POST or None)
        context = {
            'form': form
        }
        return render(request, 'budget_tracker_app/signup.html', context)


class LoginView(View):

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        context = {
            'form': form
        }
        return render(request, 'budget_tracker_app/login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
        context = {
            'form': form
        }
        return render(request, 'budget_tracker_app/login.html', context)


class LoggedIndex(View):

    def get(self, request, *args, **kwargs):
        current_date = date.today()
        expense_items = ExpenseInfo.objects.filter(user_expense=request.user, date_added=current_date).order_by('-date_added')
        budget_total = ExpenseInfo.objects.filter(user_expense=request.user, date_added=current_date).aggregate(
            budget=Sum('cost', filter=Q(cost__gt=0)))
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context = {
            'expense_items': expense_items,
            'calendar': mark_safe(html_cal),
            'prev_month': prev_month(d),
            'next_month': next_month(d),
            'budget_total': budget_total
        }
        return render(request, 'budget_tracker_app/loggedIndex.html', context)


def add_expense(request):
    form = ExpenseForm(request.POST or None)
    if request.POST and form.is_valid():
        expense_name = form.cleaned_data['expense_name']
        date_added = form.cleaned_data['date_added']
        cost = form.cleaned_data['cost']
        ExpenseInfo.objects.get_or_create(
            user_expense=request.user,
            expense_name=expense_name,
            date_added=date_added,
            cost=cost,
        )
        return HttpResponseRedirect('/')
    return render(request, 'budget_tracker_app/expense.html', {'form': form})


def expense_details(request, expense_id):
    expense = ExpenseInfo.objects.get(id=expense_id)
    context = {
        'expense': expense,
    }
    return render(request, 'budget_tracker_app/expense_detail.html', context)


class DeleteExpense(View):

    def get(self, *args, **kwargs):
        expense_id = kwargs.get('expense_id')
        expense = ExpenseInfo.objects.get(id=expense_id)
        expense.delete()
        return HttpResponseRedirect('/')


class EventEdit(generic.UpdateView):
    model = ExpenseInfo
    fields = ['expense_name', 'date_added', 'cost']
    template_name = 'budget_tracker_app/expense.html'

#
# def add_expense(request, *args, **kwargs):
#     name = request.POST['expense_name']
#     expense_cost = request.POST['cost']
#     expense_date = request.POST['expense_date']
#     ExpenseInfo.objects.create(expense_name=name, cost=expense_cost, date_added=expense_date,
#                                user_expense=request.user)
#     expense_total = ExpenseInfo.objects.filter(user_expense=request.user).aggregate(
#         expenses=Sum('cost', filter=Q(cost__lt=0)))
#     return HttpResponseRedirect('/')
