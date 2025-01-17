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
    book_ids = models.IntegerField(null=True)

    
class Readers (models.Model):
    user_name = models.CharField(max_length=255, blank=False, null=False)
    email = models.EmailField(max_length=254, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='readers/profile_picture/', null=True)
    favorite_books = models.ManyToManyField(Reader_Favorite_Books, related_name='favorite_books')
    
    
class Reviewer_Text (models.Model):
    review_text = models.TextField(max_length=500, blank=False, null=False)
    rating = models.IntegerField(null=True)
    
    
class Reviewer (models.Model):
    user_name = models.CharField(max_length=255, blank=False, null=False)
    email = models.EmailField(max_length=254, blank=True, null=True)
    reviewer_texts = models.ManyToManyField(Reviewer_Text, related_name='reviewer_text') # change to foreign key
    
    
    
class Book_Review_Page (models.Model):
    # add dynamic average rating here
    # add dynamic total readers and reveiers here
    reviewers = models.ManyToManyField(Reviewer, related_name='reviewers')
    
    
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
    
    review_page = models.ForeignKey(Book_Review_Page, on_delete=models.CASCADE, related_name='review_page', default=None)
    
    

