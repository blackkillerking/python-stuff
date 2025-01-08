import json

from django.shortcuts import render
from django.http import HttpRequest

from django.db.models.functions import JSONObject
from django.views.decorators.csrf import csrf_exempt


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializer import *



@api_view(['POST'])
def add_categories (request):
    data = request.data['data']
    print(data)
    serializer = Categories_Serializer(many=True ,data=data)
    if serializer.is_valid():
        data = serializer.data
        
        # category_obj = Categories.objects.create(
        #     name = data['name'],
        #     description = data['description'],
        #     category_image = request.FILES.get('category_image')
        #     )
    else:
        print('not good')
        
        print(serializer.errors)
    return Response(serializer.errors)
# Create your views here.
