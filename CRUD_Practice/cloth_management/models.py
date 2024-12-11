from django.db import models

# Create your models here.

class Cloth(models.Model):
    sizes={
        'XS':'XS',
        'S':'S',
        'M':'M',
        'L':'L',
        'XL':'XL',
        'XXL':'XXL',
        'd':'d'}
    
    conutry_of_orgin={
        'EG':'egypt',
        'CHA':'china',
    }
    prodcut_name=models.CharField(max_length=255)
    size=models.CharField(max_length=255, choices=sizes)
    price=models.DecimalField(max_digits=6, decimal_places=2)
    made_in=models.CharField(max_length=255, choices=conutry_of_orgin)