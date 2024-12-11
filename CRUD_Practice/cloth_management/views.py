from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import *


@api_view(['POST'])
def Add_cloth(request):
    cloth_specs=request.data
    data = Cloth.objects.create(
        prodcut_name=cloth_specs.get("product_name"),
        size=cloth_specs.get("size"),
        price=cloth_specs.get("price"),
        made_in=cloth_specs.get("made_in")
    )
    data.save
    
    return Response("Item saved")

@api_view(['GET'])
def View_cloth(request, id):
    try:
        data = Cloth.objects.get(id=id)
        cloth_data = {
            'product_name':data.prodcut_name,
            'size':data.size,
            'price':data.price,
            'made_in':data.made_in
        }
        return Response (cloth_data)
    except Cloth.DoesNotExist:
        return Response({
            'error':'This product doesnt exist'
        })
    

@api_view(['GET'])
def View_cloth_all(request):
    data = Cloth.objects.all().values()
    return Response(data)


@api_view(['PUT'])
def Update_cloth(request, id):
    try:
        data = Cloth.objects.get(id=id)
        data.prodcut_name=request.data.get("product_name")
        data.size=request.data.get("size")
        data.price=request.data.get("price")
        data.made_in=request.data.get("made_in")
    except Cloth.DoesNotExist:
        return Response({
            'error':'This product doesnt exist'
        })
    
@api_view(['DELETE'])
def Remove_cloth(request, id):
    try:
        data = Cloth.objects.get(id=id)
        data.delete()
    except Cloth.DoesNotExist:
        return Response({
            'error':'Cloth already deleted'
        })
    return Response("Cloth deleted")

# Create your views here.
