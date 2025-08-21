from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Q
from .models import Book, Review
from .forms import CustomUserCreationForm, ReviewForm, BookForm

def home(request):
    """Home page with featured books"""
    # Get 3 most recent books as featured
    featured_books = Book.objects.all()[:3]
    # Get books with highest average ratings (simplified for now)
    popular_books = Book.objects.all()[:6]
    
    return render(request, 'books/home.html', {
        'featured_books': featured_books,
        'popular_books': popular_books,
    })

def book_list(request):
    """Display all books with search functionality"""
    query = request.GET.get('search')
    if query:
        books = Book.objects.filter(
            Q(title__icontains=query) | 
            Q(author__icontains=query)
        ).distinct()
        search_performed = True
    else:
        books = Book.objects.all()
        search_performed = False
    
    return render(request, 'books/book_list.html', {
        'books': books,
        'query': query,
        'search_performed': search_performed,
    })

def book_detail(request, pk):
    """Display a single book and its reviews"""
    book = get_object_or_404(Book, pk=pk)
    reviews = book.reviews.all()
    
    # Check if current user has already reviewed this book
    user_review = None
    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()
    
    return render(request, 'books/book_detail.html', {
        'book': book,
        'reviews': reviews,
        'user_review': user_review,
    })

def register(request):
    """User registration"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'books/register.html', {'form': form})

@login_required
def add_review(request, book_id):
    """Add a review for a book"""
    book = get_object_or_404(Book, id=book_id)
    
    # Check if user has already reviewed this book
    if Review.objects.filter(book=book, user=request.user).exists():
        messages.warning(request, 'You have already reviewed this book!')
        return redirect('book_detail', pk=book_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
            messages.success(request, 'Review added successfully!')
            return redirect('book_detail', pk=book_id)
    else:
        form = ReviewForm()
    
    return render(request, 'books/add_review.html', {
        'form': form,
        'book': book,
    })

@login_required
def add_book(request):
    """Add a new book"""
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Book "{book.title}" added successfully!')
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm()
    
    return render(request, 'books/add_book.html', {'form': form})

@login_required
def edit_book(request, pk):
    """Edit an existing book"""
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Book "{book.title}" updated successfully!')
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm(instance=book)
    
    return render(request, 'books/edit_book.html', {'form': form, 'book': book})

@login_required
def delete_book(request, pk):
    """Delete a book"""
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        book_title = book.title
        book.delete()
        messages.success(request, f'Book "{book_title}" deleted successfully!')
        return redirect('book_list')
    
    return render(request, 'books/delete_book.html', {'book': book})