from django.shortcuts import render,redirect
from .forms import RegisterForm
from django.contrib import messages
def login(request):
  pass

def register(request):
  form = RegisterForm()
  if request.method == 'POST':
    form = RegisterForm(request.POST)
    if form.is_valid():
      form.save()
      messages.success(request, 'Account created! You can now log in.')
      return redirect('login_account')
    else:
      messages.error(request,"Please correct the errors below")  
      form = RegisterForm()
    
  return render(request,"register.html",{"form" : form})

def accounts(request):
  return render(request,"accounts.html")