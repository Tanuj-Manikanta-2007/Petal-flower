from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
  email = forms.EmailField(required = True)
  class Meta:
    model = User
    fields =  ['username','email']
    