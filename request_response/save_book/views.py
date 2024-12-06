from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *

# Create your views here.
@csrf_exempt
@api_view(["GET" ,"POST"])
def Get_book(request):
    try:
        data = Book.objects.get(book_name=request.data["book_name"])
    except Book.DoesNotExist:
        return Response("We will add that book")
    return Response(data)


@csrf_exempt
def Save_book(request):
    attributs = request.data
    print()
    print()
    print(attributs)
    data = Book.objects.create(book_name=attributs["book_name"], book_price=attributs["book_price"], book_lang=attributs["book_lang"])
    data.save()
    return Response("Data saved")
