# PetalCart Payment & Forms Integration Guide

## Quick Start

This guide helps you integrate the redesigned payment and form systems into your views.

---

## 1. Basic Form Implementation

### In Your View (views.py)

```python
from django.shortcuts import render
from .forms import YourForm

def your_form_view(request):
    if request.method == 'POST':
        form = YourForm(request.POST)
        if form.is_valid():
            # Process form data
            form.save()
            messages.success(request, 'Success message here')
            return redirect('success_url')
    else:
        form = YourForm()
    
    context = {
        'form': form,
        'form_title': 'Your Form Title',
        'button_text': 'Submit',
    }
    return render(request, 'form.html', context)
```

### In Your Template

```html
{% extends 'main.html' %}
{% block content %}
    {% include 'form.html' %}
{% endblock %}
```

---

## 2. Payment Page Implementation

### Payment View Example

```python
from django.shortcuts import render
from petalcart.models import Order
import razorpay

def payment_view(request, order_id):
    order = Order.objects.get(order_id=order_id)
    
    # Initialize Razorpay
    client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
    
    # Create Razorpay order
    razorpay_order = client.order.create({
        'amount': int(order.total * 100),  # Amount in paise
        'currency': 'INR',
        'receipt': str(order.order_id)
    })
    
    context = {
        'payment': order,
        'razorpay_key': RAZORPAY_KEY_ID,
    }
    return render(request, 'payment.html', context)
```

### Payment Success View

```python
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import razorpay

@csrf_exempt
def payment_success(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
        
        try:
            # Verify payment signature
            client.utility.verify_payment_signature({
                'razorpay_order_id': data['razorpay_order_id'],
                'razorpay_payment_id': data['razorpay_payment_id'],
                'razorpay_signature': data['razorpay_signature']
            })
            
            # Update order status
            order = Order.objects.get(order_id=data['razorpay_order_id'])
            order.status = 'Paid'
            order.razorpay_payment_id = data['razorpay_payment_id']
            order.razorpay_order_id = data['razorpay_order_id']
            order.save()
            
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
```

---

## 3. URL Configuration

### urls.py Example

```python
from django.urls import path
from . import views

urlpatterns = [
    # Forms
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    
    # Payment
    path('payment/<uuid:order_id>/', views.payment_view, name='payment'),
    path('payment-success/', views.payment_success, name='payment_success'),
]
```

---

## 4. Settings Configuration

### settings.py

Ensure these are configured:

```python
# Static Files
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media Files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Templates
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
            ],
        },
    },
]

# Messages
MESSAGE_TAGS = {
    'debug': 'debug',
    'info': 'info',
    'success': 'success',
    'warning': 'warning',
    'error': 'error',
}
```

---

## 5. Environment Variables

### .env File

```env
# Razorpay
RAZORPAY_KEY_ID=your_key_id
RAZORPAY_KEY_SECRET=your_key_secret

# Django
SECRET_KEY=your_secret_key
DEBUG=False  # Set to True in development
```

---

## 6. CSS Integration

### base.html (main.html) - Ensure These Links Are Present

```html
{% load static %}
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="{% static 'css/common.css' %}">
    {% block extra_css %}{% endblock %}
</head>
<body>
    {% include 'navbar.html' %}
    <main>
        {% block content %}{% endblock %}
    </main>
</body>
</html>
```

### Form Pages Auto-Include CSS

```html
{% extends 'main.html' %}

{% block extra_css %}
    <link rel="stylesheet" href="{% static 'css/forms.css' %}">
{% endblock %}

{% block content %}
    <!-- Form content -->
{% endblock %}
```

### Payment Page Auto-Includes CSS

The payment.html template automatically includes:
- `static/css/forms.css` - Form styling
- `static/css/payment.css` - Payment-specific styles

---

## 7. Form Customization Examples

### Custom Registration Form View

```python
from django.contrib.auth import authenticate, login
from accounts.forms import RegisterForm

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(
                request, 
                f'Welcome {user.username}! Your account has been created.'
            )
            login(request, user)
            return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = RegisterForm()
    
    return render(request, 'form.html', {
        'form': form,
        'form_title': 'Create Your Account',
        'button_text': 'Sign Up',
    })
```

### Custom Flower Form View

```python
from petalcart.forms import FlowerForm

def add_flower_view(request):
    if request.method == 'POST':
        form = FlowerForm(request.POST, request.FILES)
        if form.is_valid():
            flower = form.save(commit=False)
            flower.shop = request.user.flowershop  # Assuming OneToOne relationship
            flower.save()
            messages.success(request, f'Flower "{flower.flowername}" added successfully!')
            return redirect('shop_dashboard')
    else:
        form = FlowerForm()
    
    return render(request, 'form.html', {
        'form': form,
        'form_title': 'Add New Flower',
        'button_text': 'Add Flower',
    })
```

---

## 8. Template Inheritance Structure

```
main.html (extends from Django template)
├── navbar.html (included)
├── form.html (extends main.html, includes forms.css)
├── payment.html (extends main.html, includes forms.css + payment.css)
├── other templates...
└── CSS files:
    ├── static/css/common.css (base styles)
    ├── static/css/forms.css (form styling)
    ├── static/css/payment.css (payment styling)
    ├── static/css/auth.css (auth specific)
    └── static/css/home.css (home page)
```

---

## 9. Validation & Error Handling

### Display Errors in Form

The form.html template automatically displays:
- Non-field errors at the top
- Field-specific errors below inputs
- Help text for guidance
- Success/error/warning messages

### Custom Validation Example

```python
from django import forms
from accounts.forms import RegisterForm

class CustomRegisterForm(RegisterForm):
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'This email is already registered.',
                code='email_exists'
            )
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 3:
            raise forms.ValidationError(
                'Username must be at least 3 characters long.',
                code='username_too_short'
            )
        return username
```

---

## 10. Responsive Testing

### Mobile Breakpoints to Test
- **Mobile**: 320px, 375px, 480px
- **Tablet**: 768px, 1024px
- **Desktop**: 1200px, 1440px

### Test Checklist
- [ ] All inputs are clickable (44px+ height)
- [ ] Buttons are full width on mobile
- [ ] Text is readable without zoom
- [ ] Forms stack vertically on mobile
- [ ] Payment page displays correctly
- [ ] No horizontal scrolling
- [ ] Keyboard navigation works
- [ ] Focus indicators visible

---

## 11. Common Issues & Solutions

### Issue: Forms not Styling
**Solution**: 
1. Ensure `main.html` extends `base.html`
2. Check `{% load static %}` is present
3. Verify `static/css/forms.css` exists
4. Check browser console for CSS file 404s

### Issue: Payment Modal Not Opening
**Solution**:
1. Verify Razorpay key is correct
2. Check browser console for JavaScript errors
3. Ensure `https://checkout.razorpay.com/v1/checkout.js` loads
4. Test with valid amount (in paise)

### Issue: Form Validation Not Working
**Solution**:
1. Check form is properly initialized: `form = YourForm()`
2. Verify form.is_valid() is being called
3. Check cleaned_data is available
4. Ensure all required fields are present in POST

### Issue: Messages Not Displaying
**Solution**:
1. Add `{% if messages %}` block to your template
2. Configure MESSAGE_TAGS in settings.py
3. Ensure View passes messages context
4. Check message level (info, success, warning, error)

---

## 12. Security Considerations

### CSRF Protection
- Always include `{% csrf_token %}` in forms
- Configure CSRF_TRUSTED_ORIGINS in production
- Use POST for form submission, never GET

### Password Security
- Use Django's UserCreationForm
- Implement password strength validation
- Hash passwords with Django's authentication system
- Use HTTPS in production

### Payment Security
- Never log payment sensitive data
- Verify Razorpay signatures server-side
- Store only payment IDs (not card details)
- Use environment variables for API keys

---

## 13. Performance Optimization

### CSS Optimization
```python
# Compile CSS with whitenoise (already configured)
# In production, CSS is served from staticfiles/
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

### JavaScript Optimization
- Payment page script is minimal (no build step needed)
- Form.html uses vanilla JavaScript (no jQuery required)
- All animations use CSS (smoother, less JS)

---

## Quick Reference

### Form in View
```python
form = YourForm(request.POST or None)
return render(request, 'form.html', {'form': form})
```

### Payment in View
```python
return render(request, 'payment.html', {
    'payment': order,
    'razorpay_key': RAZORPAY_KEY_ID,
})
```

### Message in View
```python
messages.success(request, 'Your message here')
```

### CSS Classes for Styling
```html
<div class="form-card glass-card">
    <div class="form-group">
        <label>Your Label</label>
        <input class="form-control" type="text">
    </div>
</div>
```

---

## Support

For issues or questions:
1. Check DESIGN_SYSTEM.md for styling details
2. Review form.html for HTML structure
3. Check payment.html for payment integration
4. Consult Django documentation for views/forms
5. Review Razorpay documentation for payment setup

---

**Version**: 1.0  
**Last Updated**: February 10, 2026  
**Compatible With**: Django 3.2+, Python 3.8+
