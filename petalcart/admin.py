from django.contrib import admin

# Register your models here.
from .models import Flower,Comment,FlowerShop

admin.site.register(Flower)
admin.site.register(Comment)
admin.site.register(FlowerShop)