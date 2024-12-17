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
    prodcut_name=models.CharField(max_length=255, null=False)
    size=models.CharField(max_length=255, choices=sizes, null=False)
    price=models.DecimalField(max_digits=6, decimal_places=2, null=False)
    made_in=models.CharField(max_length=255, choices=conutry_of_orgin, null=False)
    

class Producer(models.Model):
    owner =models.CharField(max_length=255)
    company=models.CharField(max_length=255)
    cloth=models.ForeignKey(Cloth, on_delete=models.CASCADE, related_name='Prod')