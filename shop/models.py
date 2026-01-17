from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
import uuid
from petalcart.models import Flower,FlowerShop

class Stock(models.Model):
  flower = models.OneToOneField(Flower,on_delete = models.CASCADE)
  shop  = models.ForeignKey(FlowerShop,on_delete = models.CASCADE)
  quantity = models.PositiveIntegerField(default = 0)
  updated = models.DateTimeField(auto_now=True)
  created = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f"In {self.shop}  {self.flower} stock was updated to {self.quantity}"