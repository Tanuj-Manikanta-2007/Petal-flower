from django.shortcuts import render,get_object_or_404,redirect
from .models import Flower,Comment,FlowerShop,Order,OrderItem,Cart,CartItem
from .forms import CommentForm
from django.db.models import Avg
from shop.models import Stock
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required 
import razorpay,json
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
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

@login_required(login_url='login_account')
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
  
@login_required(login_url='login_account')
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, comment_id=pk)
    if request.user == comment.user:
        comment.delete()
        return redirect('home') 
    else:
        # Handle unauthorized access, e.g., redirect or show error
        return redirect('home')
    
@login_required(login_url='login_account')
def process_purchase(request,pk):
   if request.method != "POST":
      return render("home")
   flower = get_object_or_404(Flower,flower_id = pk)
   quantity = int(request.POST.get("quantity",1))
   action = request.POST.get("action") 
   try:
        stock = flower.stock   # this will raise Stock.DoesNotExist if missing
   except Stock.DoesNotExist:
        messages.error(request, "Stock is not created for this flower yet.")
        return redirect("home")

   if quantity <= 0:
      messages.error(request,"Invalid quantity.")
      return redirect("home")
   if flower.stock.quantity < quantity :
      messages.error(request,f"Only {flower.stock.quantity} in stock.")
      return redirect("home")
   
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
  flower = get_object_or_404(Flower,flower_id = flower_id)
  cart,created = Cart.objects.get_or_create(user = request.user)
  cart_item,created = CartItem.objects.get_or_create(cart = cart,flower = flower)
  cart_item.quantity += quantity
  cart_item.save()

  messages.success(request,f"{flower.flowername} added to cart")
  return redirect("cart_display")

def user_order_history(request):
   orders = Order.objects.filter(user = request.user)
   return render(request,"petalcart/order_history.html", {"orders" : orders})

@login_required(login_url='/accounts/login/')
def cart_display(request):
   cart, created = Cart.objects.get_or_create(user = request.user)
   items = cart.items.all()
   for item in items:
      item.subtotal = item.flower.price * item.quantity
   total_price = sum(item.subtotal for item in items)
   return render(request,"petalcart/cart_display.html", {"items" : items, "total_price" : total_price})

@login_required(login_url='/accounts/login/')
def checkout_cart(request):
   if request.method != 'POST' :
      return redirect('cart_view')
   if not settings.RAZORPAY_KEY_ID or not settings.RAZORPAY_KEY_SECRET:
      messages.error(request, "Razorpay keys are not configured. Please set RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET.")
      return redirect('cart_display')
   cart = get_object_or_404(Cart,user = request.user)
   cart_items = cart.items.all()
   if not cart_items :
      messages.error(request,"Your cart is empy ...")
      return redirect('cart_display')
   
   total = sum(item.flower.price * item.quantity for item in cart_items )
   order = Order.objects.create(
      user = request.user,
      total = total,
      status = "Pending"
   )

   for item in cart_items:
         OrderItem.objects.create(
         order= order,
         flower = item.flower,
         quantity = item.quantity,
         price = item.flower.price
         )

   client = razorpay.Client(
      auth = (settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET)
   )
   payment = client.order.create({
      "amount" : int(total * 10 ),
      "currency" : "INR",
      "payment_capture" : 1
   })
   order.save()
   context = {
      "order" : order,
      "payment" : payment,
       "razorpay_key" : settings.RAZORPAY_KEY_ID,
       "cart_items" : cart_items
   }
   return render(request,"payment.html",context)

def delete_cart(request, pk):
    cart_item = get_object_or_404(CartItem, id=pk, cart__user=request.user)
    cart_item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect('cart_display') 

  
def update_cart(request,pk):
   if request.method == 'POST' :
      cart_item = get_object_or_404(CartItem,id = pk)
      try:
         new_quantity = int(request.POST.get('quantity'))
      except:
         messages.error(request,"Invalid quantity .. ")
         return redirect("cart_display")
      if not hasattr(cart_item.flower,'stock'):
         messages.error(request,"This item is currently unavailable.")
         cart_item.delete()
      elif new_quantity > cart_item.flower.stock.quantity :
         messages.error(request,f"Only {cart_item.flower.stock.quantity} items left in stock . ")
      elif new_quantity <= 0:
         cart_item.delete()
         messages.info(request, " Item removes from the cart.")
      else:
         cart_item.quantity = new_quantity
         cart_item.save()
         messages.success(request,"Cart updated . ")
   return redirect('cart_display')

@csrf_exempt
def payment_sucess(request):
   data = json.loads(request.body)

   order = Order.objects.get(
      razorpay_order_id = data['razorpay_order_id']
   )

   order.razorpay_payment_id  = data['razorpay_payment_id']
   order.status = "Paid"
   order.save()

   cart = Cart.objects.get(user = order.user)
   cart.item.all().delete()

   return JsonResponse({"status" : "ok" })
