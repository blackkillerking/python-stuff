from django.urls import path
from .views import *

urlpatterns = [
    path('add_cloth/', Add_cloth, name='add_cloth'),
    path('update_cloth/<int:id>/', Update_cloth, name='update_cloth'),
    path('view_cloth/<int:id>/', View_cloth, name='view_cloth'),
    path('view_all/', View_cloth_all, name='view_all'),
    path('remove_cloth/<int:id>/', Remove_cloth, name='remove_cloth'),
]
