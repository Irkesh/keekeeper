from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<int:pk>', views.category, name='category'),
    path('delete/<int:pk>/<int:id>', views.delete, name='delete'),
    path('edit/<int:pk>/<int:id>', views.edit, name='edit'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='logout'),
    path('create_password/<int:id>/<int:user>', views.create_password, name='create_password'), # id - pk of category where to add new password item
    path('create_new_password/<int:id>', views.create_new_password, name='create_new_password'),
]

