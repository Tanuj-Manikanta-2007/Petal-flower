from django.shortcuts import render
from django.urls import path
from . import views
urlpatterns = [
  path('/',views.accounts,name = "accounts"),
  path('login/',views.login, name = "login_account"),
  path('register/',views.register, name = "register_account"),
  path('logout/',views.logout,name = "logout"),
]
