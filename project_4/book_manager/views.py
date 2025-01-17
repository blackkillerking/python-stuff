import json

from django.shortcuts import render
from django.http import HttpRequest
from django.db.models import Prefetch


from django.db.models.functions import JSONObject
from django.views.decorators.csrf import csrf_exempt


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializer import *

'''
Needed to convert data from form-data from postman into readable data
'''
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
        print(obj)
        category_obj = Categories.objects.create(
            name = obj['name'],
            description = obj['description'],
            category_image = image
            )
        print('all good')     

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



def create_tags (data):
    print()
    print('creating tags')
    print()
    for tag in data:
        tag_obj = Tags.objects.create(
            name = tag['name']
        )
        print('all good')
    
    
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
    
'''
------------------------------------------
GET SUB-FUNCTIONS
------------------------------------------
'''
'''
In a seperate function to avoid repating
'''
def prefetch_from (books):
    books_data = []

    # Go over each book to access its details
    for book in books:
        book_dict = {
            'book_id': book.id,
            'title': book.title,
            'description': book.description,
            'authors': sorted([author.name for author in book.author.all()]),  # Sorting authors
            'tags': sorted([tag.name for tag in book.tag.all()]),  # Sorting tags
            'category': sorted([category.name for category in book.category.all()]),  # Sorting categories
            'review_page': None
        }

        # Check if the book has a review page
        if book.review_page:
            review_page_dict = {
                'reviewers': []
            }

            # Loop through reviewers and their texts
            for reviewer in book.review_page.reviewers.all():
                reviewer_dict = {
                    'reviewer_name': reviewer.user_name,
                    'rating': [reviewer_text.rating for reviewer_text in reviewer.reviewer_texts.all()]
                }
                review_page_dict['reviewers'].append(reviewer_dict)

            book_dict['review_page'] = review_page_dict

        books_data.append(book_dict)
        return books_data
        
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
    # Cretes all reviewers of a review_page
    for reviewer in data['review_page']['reviewers']:
        # Cretes all texts for a reviewer
        list_of_texts =[]
        for reviewer_text in reviewer['reviewer_texts']:
            print(reviewer_text)
            reviewer_text_obj = Reviewer_Text.objects.create(
                review_text = reviewer_text['review_text'],
                rating = reviewer_text['rating'],
            )
            print(reviewer_text_obj)
            list_of_texts.append(reviewer_text_obj)

        reviewer_obj = Reviewer.objects.create(
            user_name = reviewer['user_name'],
            email = reviewer['email']
        )
         
        reviewer_obj.reviewer_texts.set(list_of_texts)
        reviewer_obj.save()
        list_of_reviewers.append(reviewer_obj)
        
    review_page_obj = Book_Review_Page.objects.create()
    
    review_page_obj.reviewers.set(list_of_reviewers)
    review_page_obj.save()
    return review_page_obj

'''
data --> serialized data from save_book()
cover_image/ sample_pdf --> send seperatly because serailzer wont see them
'''
def create_book (data, cover_image, sample_pdf):
    data = data[0]
    # We check if the data recieved is available or not
        # Get the names only to filter over them
    author_names = [d['name'] for d in data["authors"]]
    readers_user_names = [d['user_name'] for d in data['readers']]
    tag_names = [d['name'] for d in data['tags']]
    category_names = [d['name'] for d in data['categories']]
    
    print()
    print(f'{author_names}, {readers_user_names}, {tag_names}, {category_names}')
    
    authors = Author.objects.filter(name__in=author_names)
    if not authors.exists():
        return {
            'Author_doesnt_exist':'Please enter an already existing author'
        }
    readers = Readers.objects.filter(user_name__in=readers_user_names)
    if not readers.exists():
        return {
            'Reader_doesnt_exist':'Please enter an already existing reader'
        }
    tags = Tags.objects.filter(name__in=tag_names)
    if not tags.exists():
        return {
            'Tag_doesnt_exist':'Please enter an already existing tag'
        }
    categories = Categories.objects.filter(name__in=category_names)
    if not categories.exists():
        return {
            'Category_doesnt_exist':'Please enter an already existing category'
        }
        
    print()
    print(f'{authors}, {readers}, {tags}, {categories}')
    
    # After checking, we create the object
    book_obj = Book.objects.create(
        title = data['title'],
        description = data['description'],
        publication_date = data['publication_date'],
        is_published = data['is_published'],
        cover_image = cover_image,
        sample_pdf = sample_pdf,
        review_page = create_review_page(data)
        
        )
    
    book_obj.author.set(authors)
    book_obj.reader.set(readers)
    book_obj.tag.set(tags)
    book_obj.category.set(categories)
    
    book_obj.save()
    
    return (book_obj)


'''
------------------------------------------
POST FUNCTIONS
------------------------------------------
'''

'''
Creates all M2M objects at once
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
    profile_picture = request.FILES.getlist('profile_picture')
    create_readers(serializer.data, profile_picture)
    
    converted_data = convert_to_json(request.data.get('tag_data'))
    serializer = Tags_Serializer(many=True, data=converted_data)
    if not serializer.is_valid():
        return Response(serializer.errors)
    create_tags (serializer.data)
    
    converted_data = convert_to_json(request.data.get('author_data'))
    serializer = Author_Serializer(many=True, data=converted_data)
    if not serializer.is_valid():
        return Response(serializer.errors)
    create_authors (serializer.data)
    
    return Response (Categories.objects.all().values())


'''
Creates a new book
'''
@api_view(['POST'])
def save_book(request):
    converted_data = convert_to_json(request.data.get('book_data'))
    print(converted_data)
    serializer = Book_Serializer(many=True, data=converted_data)
    
    if not serializer.is_valid():
        return Response(serializer.errors)
    
    cover_image = request.FILES.get('cover_image')
    sample_pdf = request.FILES.get('sample_pdf')
    # print(serializer.data)
    # print(serializer.data[0]['authors'])
    book_obj = create_book(serializer.data, cover_image, sample_pdf)
    
    if not isinstance(book_obj, Book):
        return Response(book_obj)
    return Response (f'{book_obj.review_page}')
    

'''
------------------------------------------
GET FUNCTIONS
------------------------------------------
'''

'''
Get all data from book id
'''
@api_view(['GET'])
def view_book (request, book_id):
    data = Book.objects.select_related('review_page').prefetch_related(
            'author',
            'tag',
            'category',
            'reader',
            Prefetch('review_page__reviewers', queryset=Reviewer.objects.prefetch_related(
                Prefetch('reviewer_texts', queryset=Reviewer_Text.objects.only('review_text'))
            ))
        ).get(id=book_id)
    
    book_data = {
        'Book id': data.id,
        'Book title': data.title,
        'Book description' : data.description,
        'Book putlication date': data.publication_date,
        'Is book published?': data.is_published,
        'Book auhtors': {
            'Author(s)': data.author.all().values(),
            },
        'Book tags': {
            'Tag(s)': data.tag.all().values()
            },
        'Book categories': {
            'Categories' : data.category.all().values()
            },
        'Book readers': {
            'Reader(s)' : data.reader.all().values()
            },
        'Book review page': None
        
    }
    
    if data.review_page:
        review_page_dict = {
            'reviewers': []
        }

        # Loop through reviewers and their texts
        for reviewer in data.review_page.reviewers.all():
            reviewer_dict = {
                'reviewer_name': reviewer.user_name,
                'review_text': [reviewer_text.review_text for reviewer_text in reviewer.reviewer_texts.all()]
            }
            review_page_dict['reviewers'].append(reviewer_dict)

        book_data['Book review page'] = review_page_dict
    return Response(book_data)


'''
Get all books an author has published
'''
@api_view(['GET'])
def view_author (request, author_id):
    
#     author = Author.objects.get(id=author_id)

#     # Fetch all books related to this author with prefetching for related fields
#     books = author.author.prefetch_related(
#         'tag',               # Prefetch related tags
#         'category',           # Prefetch related categories
#         'review_page',        # Prefetch review page
#         Prefetch('review_page__reviewers', queryset=Reviewer.objects.prefetch_related(
#             Prefetch('reviewer_texts', queryset=Reviewer_Text.objects.only('review_text'))
#         ))
#     )
#     books_data = prefetch_from(books)
        
#     result_dict = {
#         'author': author.name,
#         'books': books_data
#         }
    authors = Author.objects.all().values()
    return Response(authors)
#     print(result_dict)
#     return Response(result_dict)

# '''
# Get all books of a certain category
# '''
@api_view(['GET'])
def view_category (request, category_name):
    
    category = Categories.objects.get(name=category_name)

    # Fetch all books related to this author with prefetching for related fields
    books = category.category.prefetch_related(
        'tag',               # Prefetch related tags
        'author',           # Prefetch related categories
        'review_page',        # Prefetch review page
        Prefetch('review_page__reviewers', queryset=Reviewer.objects.prefetch_related(
            Prefetch('reviewer_texts', queryset=Reviewer_Text.objects.only('review_text'))
        ))
    )

    books_data = prefetch_from(books)
    
    result_dict = {
        'author': category.name,
        'books': books_data
        }
    print(result_dict)

    
    return Response(result_dict)

'''
Get all books of a certain tag
'''
@api_view(['GET'])
def view_tag (request, tag_name):
    
    tag = Tags.objects.get(name=tag_name)

    # Fetch all books related to this author with prefetching for related fields
    books = tag.tag.prefetch_related(
        'author',               # Prefetch related tags
        'category',           # Prefetch related categories
        'review_page',        # Prefetch review page
        Prefetch('review_page__reviewers', queryset=Reviewer.objects.prefetch_related(
            Prefetch('reviewer_texts', queryset=Reviewer_Text.objects.only('review_text'))
        ))
    )
    books_data = prefetch_from(books)
        
    result_dict = {
        'author': tag.name,
        'books': books_data
        }
    print(result_dict)
    return Response(result_dict)

'''
Get all books of a certain category
'''
@api_view(['GET'])
def view_favorait_books (request, reader_id):
    
    reader = Readers.objects.prefetch_related('favorite_books').get(id=reader_id)
    print(reader.favorite_books)
    return Response('done')

'''
------------------------------------------
UPDATE FUNCTIONS
------------------------------------------
'''

'''
------------------------------------------
UPDATE MANY2MANY OBJECT
------------------------------------------
'''

# '''
# FOR SINGLE OBJECTS -->
# - Get updated data
# - Check if it exists
# - Get object needed to be updated
# - Rename each filed to the updated data
# - Save the object
# '''

# '''
# data --> has the names and discriptions of each category
# category_images --> for all categories
# '''
# def update_category (data, category, category_image):
#     print()
#     print('updating category')
#     print()
#     category.name = data['name']
#     category.description = data['description']
#     category.category_image = category_image
#     category.save()

# '''
# data --> has the usernames and emails of each reader
# profile_pictures --> ppfs for all readers
# '''
# def update_reader (data, reader, profile_picture):
#     print()
#     print('updating reader')
#     print()
#     reader.favorite_books.delete()
#     list_of_books = []
#     fav_books = data['fav_books']
#     for book in fav_books:
#         fav_book = Reader_Favorite_Books.objects.create(
#             book_id = book['book_id']
#         )
#         list_of_books.append(fav_book)
#     # check if selected books exist
    
#     reader.user_name = data['user_name']
#     reader.email = data['email']
#     reader.profile_picture = profile_picture
#     reader.favorite_books.set(list_of_books)
#     reader.save()

# def update_tag (data, tag):
#     print()
#     print('udpating tag')
#     print()
#     tag.name = data['name']
#     tag.save()
    
    
# def update_author (data, author):
#     print()
#     print('updating author')
#     print()
#     author.name = data['name']
#     author.email = data['email']
#     author.save()



# @api_view(['PUT'])    
# def update_object(request, id):
    
#     '''
#     For category
#     '''
#     converted_data = convert_to_json(request.data.get('category_data'))
#     if not converted_data:
#         return Response({
#             'Missing data':'There is no such thing as "category_data"'
#         })
        
#     category_image = request.FILES.get('category_image')
#     serializer = Categories_Serializer(data=converted_data)
#     iamge_serializer = Category_Image_Serializer(data=category_image)
    
#     if not serializer.is_valid() or not iamge_serializer.is_valid():
#         error = {
#             'Enncountered error': serializer.errors
#         }
#         return Response(error)
    
#     category = Categories.objects.get(id=id)
#     data = serializer.data
#     update_category(data, category, category_image)
    
#     '''
#     For author
#     '''
#     converted_data = convert_to_json(request.data.get('author_data'))
#     if not converted_data:
#         return Response({
#             'Missing data':'There is no such thing as "author data"'
#         })
#     serializer = Author_Serializer(data=converted_data)
#     if not serializer.is_valid():
#         return Response({
#             'Enncountered error': serializer.errors
#         })
#     author = Author.objects.get(id=id)
#     data = serializer.data
#     update_author(data, author)
    
#     '''
#     For tag
#     '''
#     converted_data = convert_to_json(request.data.get('tag_data'))
#     if not converted_data:
#         return Response({
#             'Missing data':'There is no such thing as "tag_data"'
#         })
#     serializer = Tags_Serializer(data=converted_data)
#     if not serializer.is_valid():
#         error = {
#             'Enncountered error': serializer.errors
#         }
#         return Response(error)
#     tag = Categories.objects.get(id=id)
#     data = serializer.data
#     update_tag(data, tag)
    
#     '''
#     For reader
#     '''
#     converted_data = convert_to_json(request.data.get('reader_data'))
#     if not converted_data:
#         return Response({
#             'Missing data':'There is no such thing as "reader_data"'
#         })
#     serializer = Readers_Serializer(data=converted_data)
#     if not serializer.is_valid():
#         error = {
#             'Enncountered error': serializer.errors
#         }
#         return Response(error)
#     profile_picture = request.FILES.get('profile_picture')
#     reader = Readers.objects.get(id=id)
#     data = serializer.data
#     update_reader(data, reader, profile_picture)


'''
FOR MUTLIPLE OBJECTS -->
- Get updated data
- Check if it exists
- Get the ids of the objects needed
- Get objects needed to be updated with the ids
- Rename each filed to the updated data
- Save the object
'''


def update_categories (data, category_images):
    print()
    print('updating category')
    print()
    print(data)
    ids = sorted([obj['id'] for obj in data])
    categories = Categories.objects.filter(id__in=ids)
    
    for category, category_image, obj in zip(categories, category_images, data):
        category.name = obj['name']
        category.description = obj['description']
        category.category_image = category_image
        category.save()
        
def update_authors (data):
    print()
    print('updating authors')
    print()
    
    ids = sorted([obj['id'] for obj in data])
    authors = Author.objects.filter(id__in=ids)
    
    for author, obj in zip(authors, data):
        author.name = obj['name']
        author.email = obj['description']
        author.save()


def update_tags (data):
    print()
    print('updating tags')
    print()
    
    ids = sorted([obj['id'] for obj in data])
    tags = Tags.objects.filter(id__in=ids)
    
    for tag, obj in zip(tags, data):
        tag.name = obj['name']
        tag.save()


def update_readers (data, profile_pictures):
    print()
    print('updating readers')
    print()
    
    ids = sorted([obj['id'] for obj in data])
    readers = Readers.objects.filter(id__in=ids)
    
    for reader, profile_picture, obj in zip(readers, profile_pictures, data):
        reader.user_name = obj['user_name']
        reader.email = obj['email']
        reader.profile_picture = profile_picture
        
        if obj.get('fav_books'):
            reader.favorite_books.delete()
            list_of_books = []
            fav_books = obj['fav_books']
            for book in fav_books:
                fav_book = Reader_Favorite_Books.objects.create(
                    book_id = book['book_id']
                )
                list_of_books.append(fav_book)
            reader.favorite_books.set(list_of_books)
            
        reader.save()


@api_view(['PUT'])
def update_objects (request):
    '''
    For categories
    '''
    
    if request.data.get('category_data'):
        converted_data = convert_to_json(request.data.get('category_data'))
        category_images = request.FILES.getlist('category_iamge')
        serializer = Categories_Serializer(many=True, data=converted_data)
        iamge_serializer = Category_Image_Serializer(many=True, data=category_images)
        if not serializer.is_valid() or not iamge_serializer.is_valid():
            error = {
                'Enncountered error': serializer.errors
            }
            return Response(error)
        print(request.data.get('category_data'))
        data = serializer.data
        update_categories(data, category_images)
    
    '''
    For authors
    '''
    if request.data.get('author_data'):
        converted_data = convert_to_json(request.data.get('author_data'))
        serializer = Author_Serializer(many=True, data=converted_data)
        if not serializer.is_valid():
            error = {
                'Enncountered error': serializer.errors
            }
            return Response(error)
        data = serializer.data
        update_authors(data)
    
    '''
    For tags
    '''
    
    if request.data.get('tag_data'):
        converted_data = convert_to_json(request.data.get('tag_data'))
        serializer = Categories_Serializer(many=True, data=converted_data)
        if not serializer.is_valid():
            error = {
                'Enncountered error': serializer.errors
            }
            return Response(error)
        data = serializer.data
        update_tags(data)
    
    '''
    For readers
    '''
    
    if request.data.get('reader_data'):
        converted_data = convert_to_json(request.data.get('reader_data'))
        profile_pictures = request.FILES.getlist('profile_picture')
        serializer = Categories_Serializer(many=True, data=converted_data)
        iamge_serializer = Readers_ProfilePicture_Serializer(many=True, data=profile_pictures)
        if not serializer.is_valid() or not iamge_serializer.is_valid():
            error = {
                'Enncountered error': serializer.errors
            }
            return Response(error)
        data = serializer.data
        update_readers(data, profile_pictures)
    return Response ('Objects updated')


'''
------------------------------------------
UPDATE BOOK(S) AND REVIEW PAGE(S)
------------------------------------------
'''

'''
FOR SINGLE OBJECTS -->
- Get updated data
- Check if it exists
- Get object needed to be updated
- Rename each filed to the updated data
- Save the object
'''
        
def update_review_page(data, book_obj): # DONT USE REMOVE()
    print(book_obj)
    
    review_page_obj = book_obj.review_page
    for reviewer in review_page_obj.reviewers.all():
        reviewer.reviewer_texts.remove()
    review_page_obj.reviewers.remove()
    
    list_of_reviewers = []
    # Cretes all reviewers of a review_page
    for reviewer in data['review_page']['reviewers']:
        # Cretes all texts for a reviewer
        list_of_texts =[]
        for reviewer_text in reviewer['reviewer_texts']:
            print(reviewer_text)
            reviewer_text_obj = Reviewer_Text.objects.create(
                review_text = reviewer_text['review_text'],
                rating = reviewer_text['rating'],
            )
            print(reviewer_text_obj)
            list_of_texts.append(reviewer_text_obj)

        reviewer_obj = Reviewer.objects.create(
            user_name = reviewer['user_name'],
            email = reviewer['email']
        )
        
        reviewer_obj.reviewer_texts.set(list_of_texts)
        reviewer_obj.save()
        list_of_reviewers.append(reviewer_obj)
    
    review_page_obj.reviewers.set(list_of_reviewers)
    review_page_obj.save()
    book_obj.save()
    return review_page_obj



def update_books_many2many_objects(obj, book_obj):
    
    author_names = [d['name'] for d in obj["authors"]]
    readers_user_names = [d['user_name'] for d in obj['readers']]
    tag_names = [d['name'] for d in obj['tags']]
    category_names = [d['name'] for d in obj['categories']]
    
    print()
    print(f'{author_names}, {readers_user_names}, {tag_names}, {category_names}')
    
    authors = Author.objects.filter(name__in=author_names)
    if not authors.exists():
        return {
            'Author_doesnt_exist':'Please enter an already existing author'
        }
    readers = Readers.objects.filter(user_name__in=readers_user_names)
    if not readers.exists():
        return {
            'Reader_doesnt_exist':'Please enter an already existing reader'
        }
    tags = Tags.objects.filter(name__in=tag_names)
    if not tags.exists():
        return {
            'Tag_doesnt_exist':'Please enter an already existing tag'
        }
    categories = Categories.objects.filter(name__in=category_names)
    if not categories.exists():
        return {
            'Category_doesnt_exist':'Please enter an already existing category'
        }
        
    print()
    print(f'{authors}, {readers}, {tags}, {categories}')
    
    book_obj.author.remove()
    book_obj.reader.remove()
    book_obj.tag.remove()
    book_obj.category.remove()
    
    # book_obj.author.set(authors)
    # book_obj.reader.set(readers)
    # book_obj.tag.set(tags)
    # book_obj.category.set(categories)


def update_book_info (data, cover_images, sample_pdfs):
    
    ids = sorted([obj['id'] for obj in data])
    book_objs = Book.objects.select_related('review_page').prefetch_related(
            'author',
            'tag',
            'category',
            'reader',
            Prefetch('review_page__reviewers', queryset=Reviewer.objects.prefetch_related(
                Prefetch('reviewer_texts', queryset=Reviewer_Text.objects.only('review_text'))
            ))).filter(id__in=ids)
    print(book_objs)
    for book_obj, cover_image, sample_pdf, obj in zip(book_objs, cover_images, sample_pdfs, data):
        book_obj.title = obj['title']
        book_obj.description = obj['description']
        book_obj.publication_date = obj['publication_date']
        book_obj.is_published = obj['is_published']
        book_obj.cover_image = cover_image
        book_obj.sample_pdf = sample_pdf
        update_review_page(obj, book_obj)
        update_books_many2many_objects(obj, book_obj)
        book_obj.save()


@api_view(['PUT'])
def update_books (request):
    converted_data = convert_to_json(request.data.get('book_data'))
    print(converted_data)
    serializer = Book_Serializer(many=True, data=converted_data)
    if not serializer.is_valid():
        return Response(serializer.errors)
    cover_images = request.FILES.getlist('cover_image')
    sample_pdfs = request.FILES.getlist('sample_pdf')
    data = serializer.data
    print(data)
    update_book_info(data, cover_images, sample_pdfs)
    return Response ('books updated')






























































































