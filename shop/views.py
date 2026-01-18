from django.shortcuts import render , redirect, get_object_or_404
from petalcart import models as pcmodel
from django.contrib import messages
from django.contrib.auth.models import Group
from .forms import ShopRegisterForm
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from .forms import FlowerForm, StockForm , FlowerStockForm
from .models import Stock

# Create your views here.
def shop_home(request):
  shop = get_object_or_404(pcmodel.FlowerShop,owner = request.user)
  flowers = shop.flowers.all()
  comments = pcmodel.Comment.objects.filter(flower__shop = shop)
  stocks = Stock.objects.filter(shop = shop)
  return render(request,"shop/home.html",{"flowers" : flowers,"shop" : shop,"comments" : comments , "stocks" : stocks})

def shop_register(request):
  if request.method == "POST":
    form = ShopRegisterForm(request.POST)
    if form.is_valid():
      user = form.save()
      shop_group = Group.objects.get(name = "ShopOwner")
      user.groups.add(shop_group)
      pcmodel.FlowerShop.objects.create(
        owner = user,
        shop_name = form.cleaned_data['shop_name'],
        shop_address = form.cleaned_data['shop_address']
      )
      messages.success(request,"Shop registered successfully! Login now.")
      #return redirect("shop_login")
    else:
      messages.error(request,"Please correct the erros below.")
  else:
    form = ShopRegisterForm()

  return render(request,"shop/shop_register.html",{"form" : form})

def shop_login(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    user  = authenticate(username = username,password = password)
    if user:
      if user.groups.filter(name = "ShopOwner").exists():
        login(request,user)
        messages.success(request,"Welcome back !")
        return redirect("shop_home")
      else:
        messages.error(request,"You are not registered as a shop owner.")
    else:
      messages.error(request,"Invalid username or password ")
  return render(request,"shop/shop_login.html")

def dashboard(request):
  return render(request,"shop/dashboard.html")

def createflower(request):
  form = FlowerForm()

  if request.method == 'POST':
    form = FlowerForm(request.POST, request.FILES)
    if form.is_valid():
      flower = form.save(commit = False)
      flower.shop = pcmodel.FlowerShop.objects.get(owner = request.user)
      flower.save()
      return redirect('shop_home')
     
  context = {"form" : form}
  return render(request,"shop/flower_form.html",context)

def delete_flower(request,pk):
  flower = get_object_or_404(pcmodel.Flower,flower_id = int(pk))
  if request.method == "POST":
    flower.delete()
    return redirect('shop_home')
  return render(request,'shop/delete.html',{"obj" : flower})

def update_flower(request,pk):
  flower = get_object_or_404(pcmodel.Flower, flower_id = int(pk))
  
  if request.method == "POST" :
    form = FlowerForm(request.POST,request.FILES,instance = flower)
    if form.is_valid():
      form.save()
      return redirect('shop_home')
  else:
    form = FlowerForm(instance = flower)
  return render(request,"shop/flower_form.html",{"form" : form})

def add_flower_stock(request,pk1,pk2):
  existing_stock = Stock.objects.filter(flower_id = pk2).first()
  if request.method == 'POST':
    form = FlowerStockForm(request.POST,request.FILES,instance = existing_stock)
    if form.is_valid():
      stock = form.save(commit = False)
      stock.shop = get_object_or_404(pcmodel.FlowerShop,shop_id = pk1)
      stock.flower = get_object_or_404(pcmodel.Flower,flower_id = pk2)
      stock.save()
      return redirect('shop_home')
  else:
    form = FlowerStockForm(instance = existing_stock)
  return render(request,"form.html",{"form" : form})

def add_stock(request,pk):
  shop = get_object_or_404(pcmodel.FlowerShop,shop_id = pk)
  existing_stock = Stock.objects.filter(shop=shop).first()
  if request.method == 'POST':
    form = StockForm(request.POST,request.FILES,shop = shop, instance = existing_stock)
    if form.is_valid():
      is_update = form.instance.pk is not None 
      stock = form.save(commit = False)
      stock.shop = shop
      stock.save()
      if is_update:
                messages.info(request, f"Stock for {stock.flower.flowername} was updated successfully.")
      else:
          messages.success(request, f"New stock for {stock.flower.flowername} was added.")
      return redirect('shop_home')
  else:
    form = StockForm(shop = shop, instance = existing_stock)
  
  return render(request,"form.html",{"form" : form})
  



