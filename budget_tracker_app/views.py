from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
# Create your views here.
from django.views.generic.base import View

from budget_tracker_app.forms import SignUpForm, LoginForm


class IndexView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'budget_tracker_app/index.html')


class SignUpView(View):

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST or None)
        if form.is_valid():
            User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
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
