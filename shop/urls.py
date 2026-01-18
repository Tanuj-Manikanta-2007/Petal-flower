from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
  path('',views.shop_home,name = 'shop_home'),
  path('dashboard/',views.dashboard,name = 'shop_dashboard'),
  path('register/',views.shop_register,name = "shop_register"),
  path('login/',views.shop_login,name = "shop_login"),
  path('add_flower/',views.createflower,name = "add_flower"),
  path('edit_flower/<uuid:pk>/',views.update_flower,name = "update_flower"),
  path('delete_flower/<uuid:pk>/',views.delete_flower,name = "delete_flower"),  
  path('add_flower_stock/<uuid:pk1>/<uuid:pk2>/',views.add_flower_stock,name = "add_flower_stock"),
  path('add_stock/<uuid:pk>/',views.add_stock,name ="add_stock"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)