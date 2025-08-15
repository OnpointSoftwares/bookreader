from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg, Count
from django.utils.text import slugify
from django.urls import reverse


class Genre(models.Model):
    """Model representing a book genre."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Author(models.Model):
    """Model representing an author."""
    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    death_date = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to='authors/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('author_detail', kwargs={'pk': self.pk})


class Book(models.Model):
    """Model representing a book."""
    FORMAT_CHOICES = [
        ('pdf', 'PDF'),
        ('epub', 'EPUB'),
        ('mobi', 'MOBI'),
        ('txt', 'Text'),
    ]
    
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('es', 'Spanish'),
        ('fr', 'French'),
        ('de', 'German'),
        ('zh', 'Chinese'),
        ('ja', 'Japanese'),
        ('ru', 'Russian'),
        ('ar', 'Arabic'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    description = models.TextField(blank=True)
    isbn = models.CharField('ISBN', max_length=13, unique=True, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genres = models.ManyToManyField(Genre, related_name='books')
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, default='en')
    format = models.CharField(max_length=10, choices=FORMAT_CHOICES, default='pdf')
    publisher = models.CharField(max_length=200, blank=True)
    publication_date = models.DateField(null=True, blank=True)
    page_count = models.PositiveIntegerField(null=True, blank=True)
    cover_image = models.ImageField(upload_to='book_covers/', null=True, blank=True)
    file = models.FileField(upload_to='books/')
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    review_count = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    is_popular = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['average_rating']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def update_rating(self):
        """Update the average rating and review count."""
        result = self.reviews.aggregate(average=Avg('rating'), count=Count('id'))
        self.average_rating = result['average'] or 0
        self.review_count = result['count'] or 0
        self.save(update_fields=['average_rating', 'review_count'])
    
    def get_absolute_url(self):
        return reverse('book_detail', kwargs={'slug': self.slug})
    
    def __str__(self):
        return f"{self.title} by {self.author.name}"


def user_avatar_path(instance, filename):
    # File will be uploaded to MEDIA_ROOT/avatars/user_<id>/<filename>
    return f'avatars/user_{instance.user.id}/{filename}'

class UserProfile(models.Model):
    """Extended user profile model."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(
        upload_to=user_avatar_path,
        null=True, 
        blank=True,
        help_text='Upload a profile picture (recommended size: 300x300px)'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def get_full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    def get_absolute_url(self):
        return reverse('profile')
    
    @property
    def avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url') and self.avatar.url:
            return self.avatar.url
        return '/static/images/default-avatar.png'
    
    def save(self, *args, **kwargs):
        # Delete old avatar when updating to a new one
        try:
            old_avatar = UserProfile.objects.get(pk=self.pk).avatar
            if old_avatar and old_avatar != self.avatar:
                old_avatar.delete(save=False)
        except UserProfile.DoesNotExist:
            pass
            
        super().save(*args, **kwargs)


class Bookmark(models.Model):
    """Model for users to bookmark books."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='bookmarked_by')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'book')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} bookmarked {self.book.title}"


class Review(models.Model):
    """Model for book reviews."""
    RATING_CHOICES = [
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ('user', 'book')
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.book.update_rating()
    
    def delete(self, *args, **kwargs):
        book = self.book
        super().delete(*args, **kwargs)
        book.update_rating()
    
    def __str__(self):
        return f"{self.rating} star review for {self.book.title} by {self.user.username}"


class ReadingProgress(models.Model):
    """Model to track user's reading progress for each book."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reading_progress')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reading_progress')
    current_page = models.PositiveIntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    last_read = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Reading progress'
        unique_together = ('user', 'book')
    
    def progress_percentage(self):
        if self.book.page_count and self.current_page > 0:
            return min(100, int((self.current_page / self.book.page_count) * 100))
        return 0
    
    def __str__(self):
        return f"{self.user.username}'s progress on {self.book.title}"
