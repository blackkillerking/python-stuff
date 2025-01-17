from django.urls import path
from .views import *

urlpatterns = [
    # POST methods
    path('save_many2many/', save_many2many_objects, name='save_many2many_objects'),
    path('save_book/', save_book, name='save_book'),
    # GET methods
    path('view_book/<int:book_id>/', view_book, name='view_book'),
    path('view_author/<int:author_id>/', view_author, name='view_author'),
    path('view_category/<str:category_name>/', view_category, name='view_category'),
    path('view_tag/<str:tag_name>/', view_tag, name='view_tag'),
    path('view_favorait_books/<int:reader_id>/', view_favorait_books, name='view_favorait_books'),
    # PUT methods
    path('update_objects/', update_objects, name='update_objecst'),
    path('update_books/', update_books, name='update_books'),
]