from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("This is the main page")


def cart(request):
    return  HttpResponse("This is the cart")

