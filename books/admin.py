from django.contrib import admin
from .models import Book, Review

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'genre', 'publication_date', 'created_at']
    list_filter = ['genre', 'publication_date', 'created_at']
    search_fields = ['title', 'author', 'isbn']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Review)  
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['book', 'user', 'rating', 'created_at']  # Changed from reviewer_name to user
    list_filter = ['rating', 'created_at', 'user']
    search_fields = ['book__title', 'user__username']
    readonly_fields = ['created_at', 'updated_at']