from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from petalcart.models import Flower
from django.forms import ModelForm


class ShopRegisterForm(UserCreationForm):
  shop_name = forms.CharField(max_length =255)
  shop_address = forms.CharField(max_length=2550)

  class Meta:
    model = User
    fields = ['username','email','password1','password2','shop_name','shop_address']

class FlowerForm(ModelForm):
  class Meta:
    model = Flower
    exclude = ["shop"]
    #fields = ["flowername", "img", "desc", "price"] 
