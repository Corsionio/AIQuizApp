from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Username', 'style': 'color: lightgrey;'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email', 'style': 'color: lightgrey;'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Password', 'style': 'color: lightgrey;'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm Password', 'style': 'color: lightgrey;'})

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Username', 'style': 'color: lightgrey;'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Password', 'style': 'color: lightgrey;'})

