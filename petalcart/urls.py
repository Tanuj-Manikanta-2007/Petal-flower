from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
  path('',views.home,name = 'home'),
  path('shop/<uuid:pk>/',views.shop,name = 'shop'),
  path('view_comments/',views.view_comment,name = 'view_comment'),
  path('create_comments/<uuid:pk>',views.create_comment,name = "create_comment"),
  
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)