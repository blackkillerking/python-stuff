from django.urls import path
from .views import *

urlpatterns = [
    path('save_categories/', add_categories, name='add_categories'),
    path('save_readers/', add_readers, name='add_readers'),
    path('save_tags/', add_tags, name='add_tags'),
    path('save_authors/', add_authors, name='add_authors'),
    path('save_book/', add_book, name='add_book'),
    # path('save_category/', add_categories, name='add_categories'),
    # path('save_category/', add_categories, name='add_categories'),
]