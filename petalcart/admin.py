from django.contrib import admin

# Register your models here.
from .models import Flower,Comment,FlowerShop,Order,OrderItem,Cart,CartItem

admin.site.register(Flower)
admin.site.register(Comment)
admin.site.register(FlowerShop)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(CartItem)
admin.site.register(Cart)