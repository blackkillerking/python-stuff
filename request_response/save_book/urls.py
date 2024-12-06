from .views import *
from django.urls import path, include

urlpatterns = [
    path("get_book/", Get_book, name="Get_book"),
    path("save_book/", Save_book, name="Save_book")
]
