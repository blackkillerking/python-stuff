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

# Checks if all data is given or not
def check_length (list_1, list_2, list_3, list_4, n):
    if n == 1:
        if not len(list_1) == len(list_2) == len(list_3):
            print(list_1)
            print(list_2)
            print(list_3)
            return False
    elif n == 2:
        if not len(list_1) == len(list_2) == len(list_3) == len(list_4):
            print(list_1)
            print(list_2)
            print(list_3)
            print(list_4)
            return False
    return True
        
'''
names --> names of all categories
descriptions --> for all categories
category_images --> for all categories, does save at the moment
'''
def create_categories (names, descriptions, category_images):
    for name, description, category_image in zip(names, descriptions, category_images):
        serializer = Categories_Serializer(data={"name": name, "description": description, "category_image": category_image})
        if serializer.is_valid():
            data = serializer.data
            category_obj = Categories.objects.create(
                name = data['name'],
                description = data['description'],
                category_image = data['category_image']
                )
            print('all good')
            print(Categories.objects.all().values())
           
        else:
            print('something not good')
            return serializer.errors
    return 'categories saved'

'''
usernames --> names of all readers
emails --> emails of all readers
profile_pictures --> ppfs for all readers, doesnt save atm
'''
def create_readers (usernames, emails, profile_pictures):
    for username, email, profile_picture in zip(usernames, emails, profile_pictures):
        serializer = Readers_Serializer(data={"user_name": username, "email": email, "profile_picture": profile_picture})
        if serializer.is_valid():
            data = serializer.data
            reader_favorite_books_obj = Reader_Favorite_Books.objects.create(
                book_id = None
            )
            reader_obj = Readers.objects.create(
                user_name = data['user_name'],
                email = data['email'],
                profile_picture = data['profile_picture'],
                favorite_books = reader_favorite_books_obj
                )
            print('all good')
           
        else:
            print('something not good')
            return serializer.errors
    return 'Readers saved'

'''
request --> takes the request from create_book()
sends usernames/emails/texts/ratings to create_reviewers()
'''
def create_review_page (request):
    
    # Check if all data is present
    review_usernames = request.data.getlist('review_username')
    review_emails = request.data.getlist('review_email')
    review_texts = request.data.getlist('review_text')
    review_ratings = request.data.getlist('review_rating')
    is_equal = check_length(review_usernames, review_emails, review_texts, review_ratings, 2)
    
    # Add all categories
    if is_equal:
        rev_objs = create_reviewers(review_usernames, review_emails, review_texts, review_ratings)
        serializer = Book_Reveiw_Page_Serializer(many=True, data=rev_objs)
        if serializer.is_valid():
            review_page_obj = Book_Reveiw_Page.objects.create(
                reveiwers = rev_objs
            )
            return review_page_obj
        else:
            return(f'In creating review_page--> {serializer.errors}')
    else:
        return Response({
            'Data_missing':"Please insure all data is inputed"
        })

'''
creates a reviewer object for every usernam and email
sends each review_text and review_rating to create_review_text()
'''
def create_reviewers (review_usernames, review_emails, review_texts, review_ratings):  
    list_of_reveiwers = []
    
    for review_username, review_email, review_text, review_rating in zip(review_usernames, review_emails, review_texts, review_ratings):
        serializer = Reveiwer_Serializer(data={"user_name": review_username, "email": review_email})
        if serializer.is_valid():
            data = serializer.data
            rev_obj = Reveiwer.objects.create(
                user_name = data['user_name'],
                email = data['email'],
                reveiwer_text = create_review_text(review_text, review_rating)

                )
            list_of_reveiwers.append(rev_obj)
        else:
            return(f'In creating reviewer--> {serializer.errors}')
    print('all good')
    return(list_of_reveiwers)

'''
creates a review_text object
'''
def create_review_text (review_text, review_rating):
    serializer = Reveiwer_Text_Serializer(data={"review_text": review_text, "rating": review_rating})
    if serializer.is_valid():
        data = serializer.data
        rev_text_obj = Reveiwer_Text.objects.create(
            review_text = data['review_text'],
            rating = data['rating']
        )
        return rev_text_obj
    else:
        return Response(f'In creating review_text--> {serializer.errors}')

'''
creates a book object, but is broken atm
'''
@api_view(['POST'])
def create_book (title, description, publication_date, is_published, cover_image, sample_pdf, rev_page_obj):
    serializer = Book_Serializer(data={
        "title": title, 
        "description": description, 
        "publication_date": publication_date,
        "is_published": is_published,
        "cover_image": cover_image,
        "sample_pdf": sample_pdf
        })
    
    if serializer.is_valid():
        data = serializer.data
        book_obj = Book.objects.create(
            title = data['title'],
            description = data['description'],
            publication_date = data['publication_date'],
            is_published = data['is_published'],
            cover_image = data['cover_image'],
            sample_pdf = data['sample_pdf'],
            reveiw_page = rev_page_obj,
            )
        
        
        print('all good')
        return book_obj
        
    else:
        print('something not good')
        return serializer.errors
    
'''
sets the author, category, tags, and readers of the book after said objects have been created
'''
def set_manytomany_fields (book_obj, request):
    book_authors = []
    for author in request.data.getlist('author'):
        author_instance = Author.objects.get(author['name'])
        if author_instance == None:
            return Response({
                'Author_doesnt_exist':'Please pick an existing author'
            })
        book_authors.append(author_instance)
    book_obj.author.set(book_authors)
    
    book_tags = []
    for tag in request.data.getlist('tag'):
        tag_instance = Tags.objects.get(tag['name'])
        if tag_instance == None:
            return Response({
                'Tag_doesnt_exist':'Please pick an existing tag'
            })
        book_tags.append(tag_instance)
    book_obj.tag.set(book_tags)
    
    book_categories = []
    for category in request.data.getlist('category'):
        category_instance = Categories.objects.get(category['name'])
        if category_instance == None:
            return Response({
                'Category_doesnt_exist':'Please pick an existing category'
            })
        book_categories.append(category_instance)
    book_obj.category.set(book_categories)
    
    book_readers = []
    for reader in request.data.getlist('reader'):
        reader_instance = Readers.objects.get(reader['user_name'])
        if reader_instance == None:
            return Response({
                'Reader_doesnt_exist':'Please pick an existing reader'
            })
        book_readers.append(reader_instance)
    book_obj.author.set(book_readers)
    return book_obj

# POST functions

@api_view(['POST'])
def add_categories (request):
    # Check if all data is present
    names = request.data.getlist('name')
    descriptions = request.data.getlist('description')
    images = request.FILES.getlist('category_image')
    is_equal = check_length(names, descriptions, images)
    
    # Add all categories
    if is_equal:
        return Response (create_categories(names, descriptions, images, None, 1))
    else:
        return Response({
            'Data_missing':"Please insure all data is inputed"
        })


@api_view(['POST'])
def add_readers (request):
    # Check if all data is present
    usernames = request.data.getlist('user_name')
    emails = request.data.getlist('email')
    profile_pictures = request.FILES.getlist('profile_picture')
     
    is_equal = check_length(usernames, emails, profile_pictures)
    
    # Add all readers
    if is_equal:
        return Response(create_readers(usernames, emails, profile_pictures, None, 1))
    else:
        return Response({
            'Data_missing':"Please insure all data is inputed"
        })
        
        
@api_view(['POST'])
def add_tags (request):
    serializer = Tags_Serializer(many=True, data=request.data)
    if serializer.is_valid():
        data = serializer.data
        for tag in data:
            tag_obj = Tags.objects.create(
                name = tag['name']
            )
        
        return Response('tags saved')
    else:
        return Response(serializer.errors)

        
@api_view(['POST'])
def add_authors (request):
    serializer = Author_Serializer(many=True, data=request.data)
    if serializer.is_valid():
        data = serializer.data
        for author in data:
            author_obj = Author.objects.create(
                name = author['name'],
                email = author['email']
            )
        
        return Response('authros saved')
    else:
        return Response(serializer.errors)
    

@api_view(['POST'])
def add_book (request):
    # Get book data from form-data
    
    title = request.data.get('title')
    description = request.data.get('description')
    publication_date = request.data.get('publication_date')
    is_published = request.data.get('is_published')
    cover_image = request.FILES.get('cover_image')
    sample_pdf = request.FILES.get('sample_pdf')

    rev_page_obj = create_review_page(request)
    
    book_obj = set_manytomany_fields(
        create_book(title, description, publication_date, is_published, cover_image, sample_pdf, rev_page_obj), 
        request)
    
    
    return Response(f'Book created: {book_obj}')
    





































