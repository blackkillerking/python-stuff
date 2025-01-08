from django.urls import path
from .views import *

urlpatterns = [
    path('save_category/', add_categories, name='add_categories')
]