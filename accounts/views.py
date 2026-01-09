from django.shortcuts import render,redirect
from .forms import RegisterForm
from django.contrib import auth,messages
from django.contrib.auth import authenticate,login
def login(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request,username = username,password = password)
    if user is not None:
      auth.login(request,user)
      return redirect("/")
    else:
      messages.info(request,"invalid credentails ")
      return redirect("login_account")
  return render(request,"login.html")

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

def logout(request):
  auth.logout(request)
  return redirect("/")