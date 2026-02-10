# Complete Implementation Examples

## Example 1: User Registration Flow

### accounts/views.py
```python
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.forms import RegisterForm

def register_view(request):
    """User registration with email verification"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Additional setup can go here (email verification, etc.)
            messages.success(
                request,
                f'Welcome {user.username}! Please log in with your credentials.'
            )
            return redirect('login')
        else:
            # Form errors are automatically displayed by form.html
            pass
    else:
        form = RegisterForm()
    
    return render(request, 'form.html', {
        'form': form,
        'form_title': 'Create Your Account',
        'button_text': 'Sign Up',
    })

def login_view(request):
    """User login"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'accounts/login.html')

@login_required
def logout_view(request):
    """User logout"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')
```

### accounts/urls.py
```python
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
```

---

## Example 2: Shop Owner Registration Flow

### petalcart/views.py
```python
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.contrib import messages
from petalcart.forms import ShopRegisterForm
from petalcart.models import FlowerShop

def shop_register_view(request):
    """Register as a flower shop owner"""
    if request.user.is_authenticated:
        return redirect('shop_dashboard')
    
    if request.method == 'POST':
        form = ShopRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Create FlowerShop profile
            shop_name = form.cleaned_data['shop_name']
            shop_address = form.cleaned_data['shop_address']
            
            FlowerShop.objects.create(
                shop_name=shop_name,
                shop_address=shop_address,
                owner=user
            )
            
            # Add user to ShopOwner group
            shop_owner_group, created = Group.objects.get_or_create(name='ShopOwner')
            user.groups.add(shop_owner_group)
            
            messages.success(
                request,
                f'Welcome to PetalCart, {user.username}! Your shop is ready. Please log in.'
            )
            return redirect('login')
    else:
        form = ShopRegisterForm()
    
    return render(request, 'form.html', {
        'form': form,
        'form_title': 'Register Your Flower Shop',
        'button_text': 'Create Shop Account',
    })
```

---

## Example 3: Add Flower Listing

### shop/views.py
```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from shop.forms import FlowerForm
from petalcart.models import Flower, FlowerShop

@login_required
def add_flower_view(request):
    """Add a new flower listing (shop owners only)"""
    # Check if user is shop owner
    if not request.user.groups.filter(name='ShopOwner').exists():
        raise PermissionDenied("You must be a shop owner to add flowers.")
    
    shop = FlowerShop.objects.get(owner=request.user)
    
    if request.method == 'POST':
        form = FlowerForm(request.POST, request.FILES)
        if form.is_valid():
            flower = form.save(commit=False)
            flower.shop = shop
            flower.save()
            
            messages.success(
                request,
                f'Flower "{flower.flowername}" has been added successfully!'
            )
            return redirect('shop_dashboard')
    else:
        form = FlowerForm()
    
    return render(request, 'form.html', {
        'form': form,
        'form_title': 'Add New Flower',
        'button_text': 'Add Flower to Shop',
    })

@login_required
def edit_flower_view(request, flower_id):
    """Edit flower listing"""
    flower = Flower.objects.get(flower_id=flower_id)
    
    # Authorization check
    if flower.shop.owner != request.user:
        raise PermissionDenied("You can only edit your own flowers.")
    
    if request.method == 'POST':
        form = FlowerForm(request.POST, request.FILES, instance=flower)
        if form.is_valid():
            form.save()
            messages.success(request, f'Flower "{flower.flowername}" updated successfully!')
            return redirect('shop_dashboard')
    else:
        form = FlowerForm(instance=flower)
    
    return render(request, 'form.html', {
        'form': form,
        'form_title': f'Edit {flower.flowername}',
        'button_text': 'Update Flower',
    })
```

---

## Example 4: Complete Payment Flow

### petalcart/views.py
```python
import json
import razorpay
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from petalcart.models import Order, Cart, CartItem, OrderItem
from decimal import Decimal

# Initialize Razorpay
razorpay_client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)

@login_required
def create_order_view(request):
    """Create order from cart"""
    user = request.user
    cart = Cart.objects.filter(user=user).first()
    
    if not cart or not cart.items.exists():
        messages.error(request, 'Your cart is empty.')
        return redirect('cart_display')
    
    # Calculate total
    total = sum(
        item.quantity * item.flower.price 
        for item in cart.items.all()
    )
    
    # Create Order
    order = Order.objects.create(
        user=user,
        total=total,
        status='Pending'
    )
    
    # Create OrderItems
    for cart_item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            flower=cart_item.flower,
            quantity=cart_item.quantity,
            price=cart_item.flower.price
        )
    
    # Clear cart
    cart.items.all().delete()
    
    messages.success(request, 'Order created successfully! Proceeding to payment...')
    return redirect('payment', order_id=order.order_id)

@login_required
def payment_view(request, order_id):
    """Display payment page"""
    order = Order.objects.get(order_id=order_id, user=request.user)
    
    # Create Razorpay order
    razorpay_order = razorpay_client.order.create({
        'amount': int(order.total * 100),  # Convert to paise
        'currency': 'INR',
        'receipt': str(order.order_id),
        'notes': {
            'customer_name': order.user.get_full_name() or order.user.username,
            'customer_email': order.user.email,
        }
    })
    
    # Store Razorpay order ID
    order.razorpay_order_id = razorpay_order['id']
    order.save()
    
    context = {
        'payment': order,
        'razorpay_order_id': razorpay_order['id'],
        'razorpay_key': settings.RAZORPAY_KEY_ID,
    }
    
    return render(request, 'payment.html', context)

@csrf_exempt
@require_http_methods(['POST'])
def payment_success_view(request):
    """Verify and process payment"""
    try:
        data = json.loads(request.body)
        
        # Verify signature
        razorpay_client.utility.verify_payment_signature({
            'razorpay_order_id': data['razorpay_order_id'],
            'razorpay_payment_id': data['razorpay_payment_id'],
            'razorpay_signature': data['razorpay_signature']
        })
        
        # Update order with payment info
        order = Order.objects.get(razorpay_order_id=data['razorpay_order_id'])
        order.status = 'Paid'
        order.razorpay_payment_id = data['razorpay_payment_id']
        order.save()
        
        # Send confirmation email (optional)
        # send_order_confirmation_email(order)
        
        return JsonResponse({
            'status': 'success',
            'message': 'Payment verified successfully!'
        })
    
    except razorpay.BadRequest as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Payment verification failed: {str(e)}'
        }, status=400)
    
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=500)

@login_required
def order_history_view(request):
    """View user's order history"""
    orders = Order.objects.filter(user=request.user).order_by('-created')
    
    context = {
        'orders': orders,
    }
    
    return render(request, 'petalcart/order_history.html', context)

@login_required
def order_detail_view(request, order_id):
    """View order details"""
    order = Order.objects.get(order_id=order_id, user=request.user)
    items = OrderItem.objects.filter(order=order)
    
    context = {
        'order': order,
        'items': items,
    }
    
    return render(request, 'petalcart/order_detail.html', context)
```

### petalcart/urls.py
```python
from django.urls import path
from . import views

app_name = 'petalcart'

urlpatterns = [
    # Cart
    path('cart/', views.cart_display, name='cart_display'),
    path('cart/add/<uuid:flower_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<uuid:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    
    # Orders & Payment
    path('order/create/', views.create_order_view, name='create_order'),
    path('payment/<uuid:order_id>/', views.payment_view, name='payment'),
    path('payment-success/', views.payment_success_view, name='payment_success'),
    path('order-history/', views.order_history_view, name='order_history'),
    path('order/<uuid:order_id>/', views.order_detail_view, name='order_detail'),
]
```

---

## Example 5: Complete Settings Configuration

### settings.py (Payment & Forms Section)

```python
# ============================================
# PAYMENT CONFIGURATION
# ============================================

# Razorpay Payment Gateway
RAZORPAY_KEY_ID = os.environ.get('RAZORPAY_KEY_ID')
RAZORPAY_KEY_SECRET = os.environ.get('RAZORPAY_KEY_SECRET')

RAZORPAY_WEBHOOK_SECRET = os.environ.get('RAZORPAY_WEBHOOK_SECRET')

# ============================================
# FORM CONFIGURATION
# ============================================

# Form rendering
FORM_RENDERER = 'django.forms.renderers.TemplateNameRenderer'

# Message tags for styling
MESSAGE_TAGS = {
    'debug': 'debug',
    'info': 'info',
    'success': 'success',
    'warning': 'warning',
    'error': 'error',
}

# ============================================
# AUTHENTICATION
# ============================================

# Login URL
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

# Password validators
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 8}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ============================================
# TEMPLATES
# ============================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'adaptlearn.context_processors.cart_context',
            ],
        },
    },
]

# ============================================
# STATIC & MEDIA FILES
# ============================================

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# For development
if DEBUG:
    MEDIA_ROOT = BASE_DIR / 'media'

# ============================================
# EMAIL CONFIGURATION (Optional)
# ============================================

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', True) == 'True'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = 'noreply@petalcart.com'
```

---

## Example 6: Custom Template Tags & Filters

### petalcart/templatetags/petalcart_filters.py

```python
from django import template
from django.utils.html import mark_safe

register = template.Library()

@register.filter
def currency(value):
    """Format value as Indian currency"""
    try:
        return f"₹{float(value):,.2f}"
    except (ValueError, TypeError):
        return value

@register.filter
def stars(rating):
    """Display rating as stars"""
    try:
        rating = int(rating)
        return mark_safe('⭐' * rating)
    except (ValueError, TypeError):
        return ''

@register.simple_tag
def cart_item_count(user):
    """Get cart item count for user"""
    from petalcart.models import Cart
    cart = Cart.objects.filter(user=user).first()
    if cart:
        return cart.items.count()
    return 0
```

### Use in Template

```html
{% load petalcart_filters %}

<p>Price: {{ flower.price|currency }}</p>
<p>Rating: {{ comment.rating|stars }}</p>
<p>Cart Items: {% cart_item_count user %}</p>
```

---

## Example 7: Form Error Styling

### Template Usage

```html
{% extends 'form.html' %}

{% block content %}
<!--
form.html automatically handles:
- Custom form widgets
- Error messages
- Help text
- Success messages
- Field validation
-->
{% endblock %}
```

### Custom Error Messages in forms.py

```python
from django import forms
from accounts.forms import RegisterForm

class EnhancedRegisterForm(RegisterForm):
    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 10:
            raise forms.ValidationError(
                'Password must be at least 10 characters long.',
                code='password_too_short'
            )
        if not any(char.isupper() for char in password):
            raise forms.ValidationError(
                'Password must contain at least one uppercase letter.',
                code='password_no_upper'
            )
        return password
```

---

## Example 8: Context Processors

### adaptlearn/context_processors.py

```python
from petalcart.models import Cart

def cart_context(request):
    """Add cart information to all templates"""
    cart_count = 0
    cart_total = 0
    
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            cart_count = cart.items.count()
            cart_total = sum(
                item.quantity * item.flower.price 
                for item in cart.items.all()
            )
    
    return {
        'cart_item_count': cart_count,
        'cart_total': cart_total,
    }
```

---

## Testing Examples

### tests.py

```python
from django.test import TestCase, Client
from django.contrib.auth.models import User
from petalcart.models import Order

class PaymentTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.order = Order.objects.create(
            user=self.user,
            total=1000.00,
            status='Pending'
        )
    
    def test_payment_page_loads(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(f'/payment/{self.order.order_id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'payment.html')
    
    def test_payment_context(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(f'/payment/{self.order.order_id}/')
        self.assertIn('razorpay_key', response.context)
        self.assertIn('payment', response.context)

class FormTestCase(TestCase):
    def test_register_form_valid(self):
        from accounts.forms import RegisterForm
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
        }
        form = RegisterForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_register_form_password_mismatch(self):
        from accounts.forms import RegisterForm
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'SecurePass123!',
            'password2': 'DifferentPass123!',
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
```

---

## Deployment Checklist

```
[ ] Environment variables set (.env file)
[ ] Static files collected: python manage.py collectstatic
[ ] Database migrations: python manage.py migrate
[ ] Razorpay keys configured
[ ] Email backend configured
[ ] CORS headers configured (if needed)
[ ] Debug = False in production
[ ] Secure cookie settings enabled
[ ] HTTPS enforced
[ ] Log files configured
[ ] Backup strategy planned
[ ] SSL certificate installed
[ ] Database backups scheduled
```

---

**Last Updated**: February 10, 2026
