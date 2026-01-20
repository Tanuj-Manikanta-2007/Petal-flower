from django.shortcuts import render,get_object_or_404,redirect
from .models import Flower,Comment,FlowerShop,Order,OrderItem,Cart,CartItem
from .forms import CommentForm
from django.db.models import Avg
from shop.models import Stock
from django.contrib import messages
from django.db import transaction
# Create your views here.


def home(request):
  flowers = Flower.objects.all()
  shop = FlowerShop.objects.all()
  comments = Comment.objects.all()
  for flower in flowers:
        avg_rating = flower.comments.aggregate(avg=Avg('rating'))['avg'] or 0
        flower.avg_rating = round(avg_rating)
  return render(request,"petalcart/home.html",{"flowers" : flowers, "shops" :shop, "Name" : "Tanuj","comments" : comments , "stock" : Stock })

def shop(request,pk):
  flower = get_object_or_404(Flower, flower_id=pk)
  avg_rating = flower.comments.aggregate(Avg('rating'))['rating__avg'] or 0
  return render(request, "petalcart/shop.html", {
        "flower": flower,
        "rating": avg_rating  
    })
  

def view_comment(request,pk):
  flower = get_object_or_404(Flower,flower_id = pk)
  return render(request,"shop/view_comment.html",{"flower" : flower})

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
  return render(request,"form.html",{"form" : form})

def update_comment(request,pk):
  comment = get_object_or_404(Comment,comment_id = pk)
  if request.method == "POST":
    form =  CommentForm(request.POST,instance = comment)
    if form.is_valid():
      form.save()
      return redirect('home')
  else:
    form = CommentForm(instance = comment)
    return render(request,"form.html",{"form" : form})

def delete_comment(request, pk):
    comment = get_object_or_404(Comment, comment_id=pk)
    if request.user == comment.user:
        comment.delete()
        return redirect('home') 
    else:
        # Handle unauthorized access, e.g., redirect or show error
        return redirect('home')

def process_purchase(request,pk):
   if request.method != "POST":
      return render("home")
   flower = get_object_or_404(Flower,flower_id = pk)
   quantity = int(request.POST.get("quantity",1))
   action = request.POST.get("action")
   
   if quantity <= 0:
      messages.error(request,"Invalid quantity.")
      return redirect("shop",pk)
   if flower.stock.quantity < quantity :
      messages.error(request,f"Only {flower.stock.quantity} in stock.")
      return redirect("shop",pk)
   
   if action == "add_to_cart":
      return handle_add_to_cart(request,pk,quantity)
   elif action == "buy_now" :
      return handle_buy_now(request,pk,quantity)
   else:
      messages.error(request,"Unknown action.")
      return redirect("home")
   
def handle_buy_now(request,flower_id,quantity):
   flower = get_object_or_404(Flower,flower_id = flower_id)
   with transaction.atomic():
      order = Order.objects.create(
         user = request.user,
         total = flower.price * quantity,
         status = "Pending"
      )
      OrderItem.objects.create(
         order = order,
         flower = flower,
         quantity = quantity,
         price = flower.price
      )
      flower.stock.quantity -= quantity
      flower.stock.save()

      messages.success(request,"Order placed successfully! ")
      return redirect("home")
   
def handle_add_to_cart(request,flower_id,quantity):
  flower = get_object_or_404(flower,flower_id = flower_id)
  cart,created = Cart.objects.get_or_create(user = request.user)
  cart_item,created = CartItem.objects.get_or_create(cart = cart,flower = flower)
  cart_item.quantity += quantity
  cart_item.save()

  messages.success(request,f"{flower.flowername} added to cart")
  return redirect("cart_view")
