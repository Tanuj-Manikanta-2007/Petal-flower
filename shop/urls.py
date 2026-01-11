from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
  path('',views.dashboard,name = 'shop_dashboard'),
  
  
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)