from django.contrib import admin
from .models import ProductModel


class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "available", "tag", "in_stock")


admin.site.register(ProductModel, ProductAdmin)
# Register your models here.
