from django.db import models

# Create your models here.

class Author (models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    email = models.EmailField(max_length=254, blank=True, null=True)

class Categories (models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(max_length=500, blank=False, null=False)
    category_image = models.ImageField(upload_to='category/image/', null=True)
    
class Tags (models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)

class Reader_Favorite_Books (models.Model):
    book_id = models.IntegerField(null=True)

class Readers (models.Model):
    user_name = models.CharField(max_length=255, blank=False, null=False)
    email = models.EmailField(max_length=254, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='readers/profile_picture/', null=True)
    favorite_books = models.ForeignKey(Reader_Favorite_Books, on_delete=models.CASCADE, related_name='favorite_books')
    
    
class Reveiwer_Text (models.Model):
    review_text = models.TextField(max_length=500, blank=False, null=False)
    rating = models.IntegerField(null=True)
    
    
class Reveiwer (models.Model):
    user_name = models.CharField(max_length=255, blank=False, null=False)
    email = models.EmailField(max_length=254, blank=True, null=True)
    reveiwer_text = models.OneToOneField(Reveiwer_Text, on_delete=models.CASCADE, related_name='reveiwer_text')
    
    
class Book_Reveiw_Page (models.Model):
    # add dynamic average rating here
    # add dynamic total readers and reveiers here
    reveiwers = models.ForeignKey(Reveiwer, on_delete=models.CASCADE, related_name='reveiwers')
    
    
class Book (models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(max_length=500, blank=False, null=False)
    publication_date = models.DateField()
    cover_image = models.ImageField(upload_to='book/covers/', null=False)
    sample_pdf = models.FileField(upload_to='book/samples/', null=True)
    is_published = models.BooleanField(null=False)
    
    author = models.ManyToManyField(Author, related_name='author')
    tag = models.ManyToManyField(Tags, related_name='tag')
    category = models.ManyToManyField(Categories, related_name='category')
    reader = models.ManyToManyField(Readers, related_name='reader')
    
    reveiw_page = models.OneToOneField(Book_Reveiw_Page, on_delete=models.CASCADE, related_name='reveiw_page')
    
    

