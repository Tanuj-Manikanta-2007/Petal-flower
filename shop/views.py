from django.shortcuts import render
from petalcart import models as pcmodel
# Create your views here.
def dashboard(request):
  flowers = pcmodel.Flower.objects.all()
  shops = pcmodel.FlowerShop.objects.all()
  return render(request,"shop/home.html",{"flowers" : flowers,"shops" : shops})