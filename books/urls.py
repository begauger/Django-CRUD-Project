from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('books/', views.book_list, name='book_list'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='books/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('book/<int:book_id>/review/', views.add_review, name='add_review'),
    path('book/add/', views.add_book, name='add_book'),
    path('book/<int:pk>/edit/', views.edit_book, name='edit_book'),
    path('book/<int:pk>/delete/', views.delete_book, name='delete_book'),
]