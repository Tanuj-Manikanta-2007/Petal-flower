from django.shortcuts import render,get_object_or_404,redirect
from .models import Flower,Comment,FlowerShop
from .forms import CommentForm
# Create your views here.


def home(request):
  flowers = Flower.objects.all()
  shop = FlowerShop.objects.all()
  comments = Comment.objects.all()
  return render(request,"petalcart/home.html",{"flowers" : flowers, "shops" :shop, "Name" : "Tanuj","comments" : comments })

def shop(request,pk):
  flower = get_object_or_404(Flower, flower_id=pk)
  return render(request,"petalcart/shop.html",{"flower" : flower})
  

def view_comment(request):
  flowers = Flower.objects.all()
  comments = Comment.objects.all()
  return render(request,"petalcart/view_comment.html",{"flowers" : flowers,"comments" : comments})

''' def createflower(request):
  form = FlowerForm()

  if request.method == 'POST':
    form = FlowerForm(request.POST, request.FILES)
    if form.is_valid():
      flower = form.save(commit = False)
      flower.shop = pcmodel.FlowerShop.objects.get(owner = request.user)
      flower.save()
      return redirect('shop_home')
  
  context = {"form" : form}
  return render(request,"shop/flower_form.html",context)'''

def create_comment(request,pk):
  flower = get_object_or_404(Flower,flower_id = pk)
  form = CommentForm
  if request.method == "POST":
    form = CommentForm(request.POST)
    if form.is_valid():
      comment = form.save(commit = False)
      comment.user = request.user
      comment.flower = flower
      comment.save()
      return redirect('home')
  return render(request,"comment_form.html",{"form" : form})