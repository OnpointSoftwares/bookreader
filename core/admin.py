from django.contrib import admin
from .models import Book, Author, Genre, ReadingProgress, Review, UserProfile, Bookmark
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(ReadingProgress)
admin.site.register(Review)
admin.site.register(UserProfile)
admin.site.register(Bookmark)

