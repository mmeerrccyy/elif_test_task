from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import DateInput

from budget_tracker_app.models import ExpenseInfo


class SignUpForm(UserCreationForm):
    username = forms.CharField(label='Username')

    def clean(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'The name {username} is already taken')
        password = self.cleaned_data['password1']
        confirm_password = self.clean_password2()
        # if password != confirm_password:
        # raise forms.ValidationError('Passwords don\'t match')
        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for fieldname in ['username']:
            self.fields[fieldname].help_text = None

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError('Incorrect login or password!')
        user = User.objects.filter(username=username).first()
        if user:
            if not user.check_password(password):
                raise forms.ValidationError('Incorrect login or password!')
        return self.cleaned_data

    class Meta:
        model = User
        fields = ('username', 'password')


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = ExpenseInfo
        # datetime-local is a HTML5 input type, format to make date time show on fields
        widgets = {
            'date_added': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
        exclude = ['user_expense']

    def __init__(self, *args, **kwargs):
        super(ExpenseForm, self).__init__(*args, **kwargs)
        # input_formats to parse HTML5 datetime-local input to datetime field
        self.fields['date_added'].input_formats = ('%Y-%m-%dT%H:%M',)
