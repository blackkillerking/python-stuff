from django.shortcuts import render
from django.db import IntegrityError

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import *


@api_view(['POST'])
def Add_cloth(request):
    data=request.data
    cloth_data=data.get('cloth_data')
    prod_data=data.get('prod_data')
    
    print()
    print(cloth_data.get('product_name'))
    print(cloth_data["product_name"])
    
    try:
        cloth_obj = Cloth.objects.create(
            prodcut_name=cloth_data["prodcut_name"],
            size=cloth_data["size"],
            price=cloth_data["price"],
            made_in=cloth_data["made_in"]
        )
        cloth_obj.save
        prod_obj = Producer.objects.create(
            owner=prod_data['owner'],
            company=prod_data['company'],
            cloth=cloth_obj
        )
        
        return Response("Item saved")
    
    except IntegrityError:
            return Response({
                 'error': 'Must input all parametars'
             })
            
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
        data = Producer.objects.get(id=id)
        prod_data = {
            'owner':data.owner,
            'company':data.company
        }
        return Response (f"Item found : {str(cloth_data)[1:-1]}")
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
        new_info=request.data

        try:
            
            data.prodcut_name=new_info.get("product_name")
            data.size=new_info.get("size")
            data.price=new_info.get("price")
            data.made_in=new_info.get("made_in")
            
            data.save()
            
            cloth_data = {
                'product_name':data.prodcut_name,
                'size':data.size,
                'price':data.price,
                'made_in':data.made_in
            }
            
            return Response(f"Item Updated : {str(cloth_data)[1:-1]}")
        
        except IntegrityError:
            return Response({
                 'error': 'Must input all parametars'
             })
            
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

