from django.db import models

class ProductModel(models.Model):
    name =  models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    tag = models.CharField(max_length=100)
    price = models.FloatField()
    in_stock = models.IntegerField()
    available = models.BooleanField()
    image_url = models.CharField(max_length=2083)
