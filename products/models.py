from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=255)
    description=models.CharField(max_length=255)
    country=models.CharField(max_length=255)
    size=models.CharField(max_length=255)
    image_product= models.ImageField(upload_to='products/images/', default= 'products/images/box.jpg')
    price=models.IntegerField()
