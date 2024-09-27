from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User


class RegisterForm(ModelForm):
    email = forms.EmailField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput(), max_length=50)


    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password"]

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput(), max_length=50)

    class Meta:
        fields = ['username', 'password']
