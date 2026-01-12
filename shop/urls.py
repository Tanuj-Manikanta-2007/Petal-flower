from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
  path('',views.home,name = 'shop_home'),
  path('dashboard/',views.dashboard,name = 'shop_dashboard'),
  path('register/',views.shop_register,name = "shop_register"),
  path('login/',views.shop_login,name = "shop_login"),
  path('addflower/',views.createflower,name = "add_flower"),
  
  
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)