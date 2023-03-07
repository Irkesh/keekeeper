from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<int:pk>', views.category, name='category'),
    path('delete/<int:pk>/<int:id>', views.delete, name='delete'),
    path('edit/<int:pk>/<int:id>', views.edit, name='edit'),
    path('create_password/<int:id>', views.create_password, name='create_password'), # id - pk of category where to add new password item
]