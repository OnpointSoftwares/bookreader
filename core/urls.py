from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

# Public URLs
public_patterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.custom_logout, name='logout'),
    path('books/<slug:slug>/', views.book_detail, name='book_detail'),
]

# Protected URLs (require login)
protected_patterns = [
    # Dashboard
    path('dashboard/', login_required(views.dashboard_view), name='dashboard'),
    
    # Profile
    path('profile/', login_required(views.profile_view), name='profile'),
    
    # Library
    path('my-library/', login_required(views.my_library_view), name='my_library'),
    path('update-reading-progress/<int:book_id>/<int:page>/', 
         login_required(views.update_reading_progress), 
         name='update_reading_progress'),
    path('toggle-bookmark/<int:book_id>/', 
         login_required(views.toggle_bookmark), 
         name='toggle_bookmark'),
    
    # Reading
    path('books/<slug:slug>/read/', 
         login_required(views.read_book), 
         name='read_book'),
         # Settings
path('settings/', login_required(views.settings_view), name='settings'),

]


# Combine all URL patterns
urlpatterns = public_patterns + protected_patterns
    