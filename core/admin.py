from django.contrib import admin
from .models import Anime

@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    list_display = ('title', 'content_type', 'genre', 'year', 'rating', 'is_trending', 'is_popular', 'is_new')
    list_filter = ('content_type', 'genre', 'is_trending', 'is_popular', 'is_new')
    search_fields = ('title', 'description')