from django.urls import path
from .views import *

urlpatterns = [
    path('save_many2many/', save_many2many_objects, name='save_many2many_objects'),
    path('save_book/', save_book, name='save_book')

]