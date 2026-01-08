from django.shortcuts import render,get_object_or_404
from .models import Flower,Comment,FlowerShop
# Create your views here.


def home(request):
  flowers = Flower.objects.all()
  shop = FlowerShop.objects.all()
  return render(request,"petalcart/home.html",{"flowers" : flowers, "shops" :shop, "Name" : "Tanuj" })

def shop(request,pk):
  flower = get_object_or_404(Flower, flower_id=pk)
  return render(request,"petalcart/shop.html",{"flower" : flower})
  

