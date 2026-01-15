from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
import uuid
# Create your models here.

class FlowerShop(models.Model):
  shop_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  shop_name = models.CharField(max_length=255)
  shop_address = models.CharField(max_length=255)
  owner = models.OneToOneField(User, on_delete=models.CASCADE,
                               null = True , blank = True )
  def __str__(self):
    return self.shop_name
  
class Flower(models.Model):
  shop = models.ForeignKey(FlowerShop, on_delete=models.CASCADE,
                          related_name='flowers',null=True,blank = True) 
  # Allows existing flowers to remain if you don't have shop data yeblank=True
  flower_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  flowername = models.CharField(max_length=100) 
  img = models.ImageField(upload_to='pics/')
  desc = models.TextField()
  price = models.DecimalField(max_digits=10, decimal_places=2)
  updated = models.DateTimeField(auto_now=True)
  created = models.DateTimeField(auto_now_add=True)

  def __str__(self):
      return self.flowername

class Comment(models.Model):
    comment_id = models.UUIDField(primary_key = True,default = uuid.uuid4,editable= False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    # Adding related_name allows flower.comments.all()
    flower = models.ForeignKey(
        Flower, 
        on_delete=models.CASCADE, 
        related_name='comments'
    )
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # FIX: Changed self.flower.name to self.flower.flowername
        return f'Comment by {self.user.username} on {self.flower.flowername}'