from rest_framework import serializers
from .models import *


class Author_Serializer (serializers.Serializer):
    name = serializers.CharField(max_length=255, allow_blank=False, allow_null=False, required=True)
    email = serializers.EmailField(max_length=254, allow_blank=True, allow_null=True, required=False)
    
    def to_internal_value(self, data):
        if data['email'] == "":
            data['email'] = None
        return super().to_internal_value(data)
    
    def validate(self, data):
        if data['name'] == "" or None:
            raise serializers.ValidationError({
                'Author_name':"Must input the author's name"
            })
        return data
    
class Categories_Serializer (serializers.Serializer):
    name = serializers.CharField(max_length=255, allow_blank=False, allow_null=False, required=True)
    description = serializers.CharField(max_length=500, allow_blank=False, allow_null=False, required=True)
    # category_image = serializers.ImageField(upload_to='category/image/', allow_null=False, required=True)
    
    def validate(self, data):
        if data['name'] == "" or None:
            raise serializers.ValidationError({
                'Category_name':"Must input a category name"
            })
        if data['description'] == "" or None:
            raise serializers.ValidationError({
                'Category_description':"Must input a category description"
            })
        # if data['category_image'] == None:
        #     raise serializers.ValidationError({
        #         'Category_category_image':"Must input a category image"
        #     })
        return data


class Tags_Serializer (serializers.Serializer):
    name = serializers.CharField(max_length=255, allow_blank=False, allow_null=False, required=True)
    
    def validate(self, data):
        if data['name'] == "" or None:
            raise serializers.ValidationError({
                'Tag_name':"Must input a tag name"
            })
        return data
    
class Reader_Favorite_Books_Serializer (serializers.Serializer):
    book_id = serializers.IntegerField(allow_null=True, required=False)
    
class Readers_Serializer (serializers.Serializer):
    user_name = serializers.CharField(max_length=255, allow_blank=False, allow_null=False, required=True)
    email = serializers.EmailField(max_length=254, allow_blank=True, allow_null=True, required=False)
    profile_picture = serializers.ImageField(allow_null=True, required=False)
    favorite_books = Reader_Favorite_Books_Serializer(many=True)
    
    def validate(self, data):
        if data['user_name'] == "" or None:
            raise serializers.ValidationError({
                'Reader_user_name':'Must input a reader username'
            })
        if data['profile_picture'] == None:
            raise serializers.ValidationError({
                'Reader_profile_picture':'Must input a reader profile picture'
            })
        return data
    
class Reveiwer_Text_Serializer (serializers.Serializer):
    review_text = serializers.CharField(max_length=255, allow_blank=False, allow_null=False, required=True)
    rating = serializers.IntegerField(allow_null=True, required=False)
    
    def to_internal_value(self, data):
        if data['rating'] == None:
            data['rating'] = None
        return super().to_internal_value(data)
    
    def validate(self, data):
        if data['review_text'] == "" or None:
            raise serializers.ValidationError({
                'Review_text':'Must input a review'
            })
        if data['rating'] not in [1, 2, 3, 4, 5]:
            raise serializers.ValidationError({
                'Invalid_rating':'Must input a rating between 1 and 5'
            })
        return data
    
class Reveiwer_Serializer (serializers.Serializer):
    user_name = serializers.CharField(max_length=255, allow_blank=False, allow_null=False, required=True)
    email = serializers.EmailField(max_length=254, allow_blank=True, allow_null=True, required=False)
    reveiwer_text = Reveiwer_Text_Serializer()
    
    def validate(self, data):
        if data['user_name'] == "" or None:
            raise serializers.ValidationError({
                'Reveiwer_username':'Must input a reveiwer name'
            })
        return super().validate(data)
    
class Book_Reveiw_Page_Serializer (serializers.Serializer):
    reveiwers = Reveiwer_Serializer(many=True)
    
class Book_Serializer (serializers.Serializer):
    title = serializers.CharField(max_length=255, allow_blank=False, allow_null=False, required=True)
    description = serializers.CharField(max_length=500, allow_blank=False, allow_null=False, required=True)
    publication_date = serializers.DateField()
    cover_image = serializers.ImageField(allow_null=False, required=True)
    sample_pdf = serializers.FileField(allow_null=True, required=False)
    is_published = serializers.BooleanField(allow_null=False, required=True)
    
    author = Author_Serializer(many=True)
    tag = Tags_Serializer(many=True)
    category = Categories_Serializer(many=True)
    reader = Readers_Serializer(many=True)
    
    reveiw_page = Book_Reveiw_Page_Serializer()
    
    def validate(self, data):
        if data['title'] == "" or None:
            raise serializers.ValidationError({
                'Book_title':"Must input the book's title"
            })
        if data['description'] == "" or None:
            raise serializers.ValidationError({
                'Book_description':"Must input a book description"
            })
        if data['publication_date'] == None:
            raise serializers.ValidationError({
                'Book_publication_date':"Must input the book's publication_date"
            })
        if data['cover_image'] == None:
            raise serializers.ValidationError({
                'Book_cover_image':"Must input the book's cover image"
            })
        if data['is_published'] == None:
             raise serializers.ValidationError({
                'Book_is_published':"Must speicify if the book is published"
            })
        if data['is_published'] not in [True, False]:
             raise serializers.ValidationError({
                'Invalid_input':"Must speicify if the book is published"
            })
        
        return super().validate(data)
    
    
class Author_ModelSerializer (serializers.ModelSerializer):
    class Meta:
        model = Author
        field = ['id','name', 'email']
        
class Categories_ModelSerializer (serializers.ModelSerializer):
    class Meta:
        model = Categories
        field = ['id', 'name', 'description', 'category_image']
        
class Tags_ModelSerializer (serializers.ModelSerializer):
    class Meta:
        model = Tags
        field = ['id', 'name']
    
class Reader_Favorite_Books_ModelSerializer (serializers.ModelSerializer):
    class Meta:
        model = Reader_Favorite_Books
        field = ['id', 'book_id']

class Readers_ModelSerializer (serializers.ModelSerializer):
    favorite_books = Reader_Favorite_Books_ModelSerializer(many=True)
    class Meta:
        model = Readers
        field = ['id', 'user_name', 'email', 'profile_picture', 'favorite_books']
        
class Reveiwer_Text_ModelSerializer (serializers.ModelSerializer):
    class Meta:
        model = Reveiwer_Text
        field = ['id', 'review_text', 'rating']
        
class Reveiwer_ModelSerializer (serializers.ModelSerializer):
    reveiwer_text = Reveiwer_Text_ModelSerializer()
    class Meta:
         model = Reveiwer
         field = ['id', 'user_name', 'email', 'reveiwer_text']
         
class Book_Reveiw_Page_ModelSerializer (serializers.ModelSerializer):
    reveiwers = Reveiwer_ModelSerializer(many=True)
    class Meta:
        model = Book_Reveiw_Page
        field = ['id', 'reveiwers']
        
class Book_ModelSerializer (serializers.ModelSerializer):
    author = Author_ModelSerializer(many=True)
    tag = Tags_ModelSerializer(many=True)
    category = Categories_ModelSerializer(many=True)
    reader = Readers_ModelSerializer(many=True)
    
    reveiw_page = Book_Reveiw_Page_ModelSerializer()
    
    class Meta:
        model = Book
        fields = ['id', 
                  'title', 
                  'description', 
                  'publication_date', 
                  'cover_image', 
                  'sample_pdf', 
                  'is_published',
                  'author',
                  'tag',
                  'category',
                  'reader',
                  'reveiw_page']
    

    
    
    
    