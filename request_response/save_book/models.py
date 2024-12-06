from django.db import models

# Create your models here.


class Book(models.Model):
    lang={
        "EN":"english",
        "AR":"arabic",
        "FR":"french",
        "SP":"spanish"
    }
    
    book_name=models.CharField(max_length=255)
    book_price=models.DecimalField(max_digits=255, decimal_places=2)
    book_lang=models.CharField(max_length=255, choices=lang)