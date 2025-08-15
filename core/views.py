from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from django.utils import timezone
from django.db.models import Count, Avg
from django.contrib.auth.forms import PasswordChangeForm
from .forms import LoginForm, SignUpForm, ProfileForm, UserForm
from .models import Book, UserProfile, ReadingProgress, Bookmark, Review
from django.views.decorators.http import require_http_methods
def home(request):
    books = Book.objects.all()
    return render(request, 'core/home.html', {'books': books})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        messages.error(request, 'Invalid form data')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
@login_required
def dashboard_view(request):
    """User dashboard view showing reading statistics and recent activity."""
    context = {
        'recent_books': Book.objects.filter(reading_progress__user=request.user)
                                  .order_by('-reading_progress__last_read')[:5],
        'reading_stats': {
            'total_books': Book.objects.filter(reading_progress__user=request.user).count(),
            'completed_books': Book.objects.filter(reading_progress__user=request.user, 
                                                reading_progress__is_completed=True).count(),
            'in_progress': Book.objects.filter(reading_progress__user=request.user, 
                                            reading_progress__is_completed=False).count(),
            'total_pages': sum(book.page_count or 0 for book in 
                             Book.objects.filter(reading_progress__user=request.user))
        },
        'recent_activity': [],  # You can add recent activity tracking here
    }
    return render(request, 'profile/dashboard.html', context)

@login_required
def profile_view(request):
    """User profile view and update form."""
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # If profile doesn't exist, redirect to settings to create one
        return redirect('settings')
        
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    
    context = {
        'form': form,
        'profile': profile
    }
    return render(request, 'profile/profile.html', context)

@login_required
def my_library_view(request):
    """View showing user's library with reading progress."""
    # Get books with reading progress
    books = Book.objects.filter(reading_progress__user=request.user)
    
    # Get bookmarked books through the Bookmark model
    bookmarked_books = Book.objects.filter(
        id__in=Bookmark.objects.filter(user=request.user).values('book_id')
    ).order_by('-bookmarked_by__created_at')
    
    # Group books by status
    reading_lists = {
        'currently_reading': books.filter(reading_progress__is_completed=False)
                                .order_by('-reading_progress__last_read'),
        'completed': books.filter(reading_progress__is_completed=True)
                        .order_by('-reading_progress__last_read'),
        'bookmarked': bookmarked_books,
    }
    
    return render(request, 'profile/mylibrary.html', {
        'reading_lists': reading_lists
    })

@login_required
def update_reading_progress(request, book_id, page):
    """Update reading progress for a book."""
    book = get_object_or_404(Book, id=book_id)
    reading_progress, created = ReadingProgress.objects.get_or_create(
        user=request.user,
        book=book,
        defaults={'current_page': page}
    )
    
    if not created:
        reading_progress.current_page = page
        if book.page_count and page >= book.page_count * 0.95:  # Consider 95% as completed
            reading_progress.is_completed = True
            reading_progress.completed_at = timezone.now()
        reading_progress.save()
    
    return redirect('my_library')

@login_required
def toggle_bookmark(request, book_id):
    """Add or remove a bookmark for a book."""
    book = get_object_or_404(Book, id=book_id)
    bookmark, created = Bookmark.objects.get_or_create(
        user=request.user,
        book=book
    )
    
    if not created:
        bookmark.delete()
        messages.success(request, 'Bookmark removed.')
    else:
        messages.success(request, 'Book added to your library!')
    
    return redirect('book_detail', slug=book.slug)

def custom_logout(request):
    """Custom logout view to handle logout and redirect."""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('home')

@login_required
def settings_view(request):
    """View for user settings and preferences."""
    user = request.user
    
    # Get or create user profile
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    
    # Initialize forms with POST data if available
    if request.method == 'POST':
        # Handle profile update
        if 'update_profile' in request.POST:
            user_form = UserForm(request.POST, instance=user)
            profile_form = ProfileForm(
                request.POST, 
                request.FILES, 
                instance=user_profile
            )
            
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, 'Your profile has been updated!')
                return redirect('settings')
            else:
                messages.error(request, 'Please correct the errors below.')
        
        # Handle password change
        elif 'change_password' in request.POST:
            password_form = PasswordChangeForm(user=user, data=request.POST)
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, password_form.user)  # Keep the user logged in
                messages.success(request, 'Your password was successfully updated!')
                return redirect('settings')
            else:
                messages.error(request, 'Please correct the error(s) below.')
    
    # Initialize empty forms for GET requests or if not in POST data
    user_form = user_form if 'user_form' in locals() else UserForm(instance=user)
    profile_form = profile_form if 'profile_form' in locals() else ProfileForm(instance=user_profile)
    password_form = password_form if 'password_form' in locals() else PasswordChangeForm(user=user)
    
    # Add form-control class to all form fields
    for field in password_form.fields.values():
        field.widget.attrs['class'] = 'form-control'
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'form': password_form,  # For password change form
        'profile_created': created,
    }
    
    return render(request, 'profile/settings.html', context)

def book_detail(request, slug):
    """View for displaying book details."""
    book = get_object_or_404(Book, slug=slug)
    reading_progress = None
    is_bookmarked = False
    
    if request.user.is_authenticated:
        reading_progress = ReadingProgress.objects.filter(
            user=request.user, 
            book=book
        ).first()
        
        is_bookmarked = Bookmark.objects.filter(
            user=request.user, 
            book=book
        ).exists()
    
    context = {
        'book': book,
        'reading_progress': reading_progress,
        'is_bookmarked': is_bookmarked,
    }
    
    return render(request, 'books/detail.html', context)

@login_required
def read_book(request, slug):
    """View for reading a book using PDF.js."""
    book = get_object_or_404(Book, slug=slug)
    
    # Update or create reading progress
    reading_progress, created = ReadingProgress.objects.get_or_create(
        user=request.user,
        book=book,
        defaults={'last_page': 1, 'is_completed': False}
    )
    
    # If this is a POST request, update the reading progress
    if request.method == 'POST':
        page = int(request.POST.get('page', 1))
        is_completed = request.POST.get('is_completed', 'false').lower() == 'true'
        
        reading_progress.last_page = page
        reading_progress.is_completed = is_completed
        reading_progress.last_read = timezone.now()
        reading_progress.save()
        
        return JsonResponse({'status': 'success'})
    
    # For GET request, render the read template
    context = {
        'book': book,
        'current_page': reading_progress.last_page,
        'is_bookmarked': Bookmark.objects.filter(user=request.user, book=book).exists(),
    }
    
    return render(request, 'books/read.html', context)
def settings_view(request):
    """View for user settings."""
    return render(request, 'profile/settings.html')