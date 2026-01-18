from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from petalcart.models import Flower 
from django.forms import ModelForm
from .models import Stock


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

class FlowerStockForm(ModelForm):
  class Meta:
    model = Stock
    exclude = ["flower", "shop"]

class StockForm(ModelForm):
  class Meta:
    model = Stock
    exclude = ["shop"]

  def __init__(self , *args,shop = None, **kwargs):
    super().__init__(*args, **kwargs)

    if shop:
      self.fields['flower'].queryset = Flower.objects.filter(shop = shop)

