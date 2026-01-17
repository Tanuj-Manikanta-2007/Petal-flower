from django.shortcuts import render,get_object_or_404,redirect
from .models import Flower,Comment,FlowerShop
from .forms import CommentForm
from django.db.models import Avg
# Create your views here.


def home(request):
  flowers = Flower.objects.all()
  shop = FlowerShop.objects.all()
  comments = Comment.objects.all()
  for flower in flowers:
        avg_rating = flower.comments.aggregate(avg=Avg('rating'))['avg'] or 0
        flower.avg_rating = round(avg_rating)
  return render(request,"petalcart/home.html",{"flowers" : flowers, "shops" :shop, "Name" : "Tanuj","comments" : comments })

def shop(request,pk):
  flower = get_object_or_404(Flower, flower_id=pk)
  avg_rating = flower.comments.aggregate(Avg('rating'))['rating__avg'] or 0
  return render(request, "petalcart/shop.html", {
        "flower": flower,
        "rating": avg_rating  
    })
  

def view_comment(request,pk):
  flower = get_object_or_404(Flower,flower_id = pk)
  return render(request,"petalcart/view_comment.html",{"flower" : flower})

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
      rating = request.POST.get("rating")
      # If rating is None or empty → set to 0
      comment.rating = int(rating) if rating else 0
      comment.user = request.user
      comment.flower = flower
      comment.save()
      return redirect('home')
  return render(request,"comment_form.html",{"form" : form})

def update_comment(request,pk):
  comment = get_object_or_404(Comment,comment_id = pk)
  if request.method == "POST":
    form =  CommentForm(request.POST,instance = comment)
    if form.is_valid():
      form.save()
      return redirect('home')
  else:
    form = CommentForm(instance = comment)
    return render(request,"comment_form.html",{"form" : form})

def delete_comment(request, pk):
    comment = get_object_or_404(Comment, comment_id=pk)
    if request.user == comment.user:
        comment.delete()
        return redirect('home') 
    else:
        # Handle unauthorized access, e.g., redirect or show error
        return redirect('home')