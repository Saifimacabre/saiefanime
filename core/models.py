from django.db import models

class Anime(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    poster = models.ImageField(upload_to='posters/', blank=True, null=True)
    
    genre = models.CharField(max_length=100, blank=True)
    year = models.IntegerField()
    rating = models.FloatField(default=7.5)
    episodes = models.IntegerField(default=12)
    
    # New fields
    is_trending = models.BooleanField(default=False)
    is_popular = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    
    # Important: Series or Movie
    CONTENT_TYPE_CHOICES = [
        ('series', 'Series'),
        ('movie', 'Movie'),
    ]
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPE_CHOICES, default='series')
    
    trailer_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-rating']