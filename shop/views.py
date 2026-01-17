from django.shortcuts import render , redirect, get_object_or_404
from petalcart import models as pcmodel
from django.contrib import messages
from django.contrib.auth.models import Group
from .forms import ShopRegisterForm
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from .forms import FlowerForm
# Create your views here.
def home(request):
  flowers = pcmodel.Flower.objects.all()
  shops = pcmodel.FlowerShop.objects.all()
  comments = pcmodel.Comment.objects.all()
  return render(request,"shop/home.html",{"flowers" : flowers,"shops" : shops,"comments" : comments})

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





