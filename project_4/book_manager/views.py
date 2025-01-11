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


def convert_to_json(data):
    string_list = [
        data
    ]
    json_objects = [json.loads(s) for s in string_list] # DONT LOSE OR DELETE
    returned_data = json_objects[0]['data']
    return returned_data

'''
------------------------------------------
CREATE MANY2MANY OBJECTS
------------------------------------------
'''

'''
data --> has the names and discriptions of each category
category_images --> for all categories
'''
def create_categories (data, category_images):
    print()
    print('creating categories')
    print()
    for obj, image in zip(data, category_images):
        category_obj = Categories.objects.create(
            name = obj['name'],
            description = obj['description'],
            category_image = image
            )
        print('all good')     
    return 'categories saved'

'''
data --> has the usernames and emails of each reader
profile_pictures --> ppfs for all readers
'''
def create_readers (data, profile_pictures):
    print()
    print('creating readers')
    print()
    for obj, image in zip(data, profile_pictures):
        reader_obj = Readers.objects.create(
            user_name = obj['user_name'],
            email = obj['email'],
            profile_picture = image
            )
        print('all good')
    return 'readers saved'



def create_tags (data):
    print()
    print('creating tags')
    print()
    for tag in data:
        tag_obj = Tags.objects.create(
            name = tag['name']
        )
        print('all good')
    return 'tags saved'
    
    
def create_authors (data):
    print()
    print('creating authors')
    print()
    for author in data:
        author_obj = Author.objects.create(
            name = author['name'],
            email = author['email']
        )
        print('all good')
    return 'authors saved'
    

'''
------------------------------------------
CREATE functions
------------------------------------------
'''
'''
data --> has the reiveiwer's usernam, email, text and rating
'''
def create_review_page(data):
    list_of_reviewers = []
    for reveiwer in data['review_page']:
        list_of_texts =[]
        for reveiwer_text in reveiwer['reveiwer_texts']:
            reviewer_text_obj = Reviewer_Text.objects.create(
                review_text = reveiwer_text['review_text'],
                rating = reveiwer_text['rating']
            )
            list_of_texts.append(reviewer_text_obj)
            
        reviewer_obj = Reviewer.objects.create(
            user_name = reveiwer['user_name'],
            email = reveiwer['email'],
            reveiwer_texts = list_of_texts,   
        )
        list_of_reviewers.append(reviewer_obj)
        
    review_page_obj = Book_Review_Page.objects.create(
        reviewers = list_of_reviewers
    )
    return review_page_obj

def create_book (data, cover_image, sample_pdf):
    book_obj = Book.objects.create(
        title = data['title'],
        description = data['description'],
        publication_date = data['publication_date'],
        is_published = data['is_published'],
        cover_image = cover_image,
        sample_pdf = sample_pdf,
        
        reveiw_page = create_review_page(data)
        
        )
    list_authors = []
    for author in data['authors']:
        author_obj = Author.objects.filter(name=author['name'])
        list_authors.append(author_obj)
    book_obj.author.set(list_authors)
    return (book_obj)


'''
------------------------------------------
POST FUNCTIONS
------------------------------------------
'''

@api_view(['POST'])
def save_many2many_objects (request):
    
    converted_data = convert_to_json(request.data.get('category_data'))
    serializer = Categories_Serializer(many=True, data=converted_data)
    if not serializer.is_valid():
        return Response(serializer.errors)
    category_images = request.FILES.getlist('category_image')
    create_categories (serializer.data, category_images)
    
    converted_data = convert_to_json(request.data.get('reader_data'))
    serializer = Readers_Serializer(many=True, data=converted_data)
    if not serializer.is_valid():
        return Response(serializer.errors)
    category_images = request.FILES.getlist('profile_picture')
    create_categories (serializer.data, category_images)
    
    converted_data = convert_to_json(request.data.get('tag_data'))
    serializer = Tags_Serializer(many=True, data=converted_data)
    if not serializer.is_valid():
        return Response(serializer.errors)
    create_categories (serializer.data)
    
    converted_data = convert_to_json(request.data.get('author_data'))
    serializer = Author_Serializer(many=True, data=converted_data)
    if not serializer.is_valid():
        return Response(serializer.errors)
    create_categories (serializer.data, category_images)
    
    return Response (Categories.objects.all().values())


@api_view(['POST'])
def save_book(request):
    converted_data = convert_to_json(request.data.get('book_data'))
    print(converted_data[0]['authors'])
    serializer = Book_Serializer(many=True, data=converted_data)
    if not serializer.is_valid():
        return Response(serializer.errors)
    cover_image = request.FILES.get('cover_image')
    sample_pdf = request.FILES.get('sample_pdf')
    book_obj = create_book(serializer.data, cover_image, sample_pdf)
    return Response (serializer.data)
    







