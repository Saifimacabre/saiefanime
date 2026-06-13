from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from .models import Anime
from django.db import models   # Add this import at the top if not there
from django.core.mail import send_mail
from django.conf import settings
def landing(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'landing.html')

def home(request):
    if not request.user.is_authenticated:
        return redirect('landing')
    
    trending = Anime.objects.filter(is_trending=True)[:12]
    popular = Anime.objects.filter(is_popular=True)[:12]
    
    return render(request, 'home.html', {
        'username': request.user.username,
        'trending_anime': trending,
        'all_anime': popular,
        'page_title': 'Home'
    })

def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to SaiefAnime, {user.username}!")
            return redirect('home')
    else:
        form = UserCreationForm()
    
    return render(request, 'signup.html', {'form': form})

def watch(request, anime_id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    try:
        anime = Anime.objects.get(id=anime_id)
        # Simple recommendations (same genre or trending)
        recommendations = Anime.objects.filter(genre=anime.genre).exclude(id=anime.id)[:6]
    except Anime.DoesNotExist:
        anime = None
        recommendations = []
    
    return render(request, 'watch.html', {
        'anime': anime,
        'recommendations': recommendations
    })
# New Pages
def series(request):
    if not request.user.is_authenticated:
        return redirect('login')
    series_list = Anime.objects.filter(content_type='series')
    return render(request, 'home.html', {
        'username': request.user.username,
        'trending_anime': series_list,
        'all_anime': series_list,
        'page_title': 'Series'
    })

def movies(request):
    if not request.user.is_authenticated:
        return redirect('login')
    movies_list = Anime.objects.filter(content_type='movie')
    return render(request, 'home.html', {
        'username': request.user.username,
        'trending_anime': movies_list,
        'all_anime': movies_list,
        'page_title': 'Movies'
    })

def new_popular(request):
    if not request.user.is_authenticated:
        return redirect('login')
    new_list = Anime.objects.filter(is_new=True)
    return render(request, 'home.html', {
        'username': request.user.username,
        'trending_anime': new_list,
        'all_anime': Anime.objects.all()[:12],
        'page_title': 'New & Popular'
    })

def my_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'home.html', {
        'username': request.user.username,
        'trending_anime': [],
        'all_anime': [],
        'page_title': 'My List'
    })
def search(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    query = request.GET.get('q', '').strip()
    results = Anime.objects.none()
    
    if query:
        results = Anime.objects.filter(
            models.Q(title__icontains=query) | 
            models.Q(genre__icontains=query) |
            models.Q(description__icontains=query)
        )
    
    return render(request, 'home.html', {
        'username': request.user.username,
        'trending_anime': results,
        'all_anime': results,
        'page_title': f'Search Results for "{query}"' if query else 'Search'
    })
def send_new_anime_notification(anime):
    """Send email to all users when new anime is added"""
    users = User.objects.all()  # Import User at top: from django.contrib.auth.models import User
    
    subject = f"New Anime Added: {anime.title}"
    message = f"""
    Hello,

    A new anime has been added to SaiefAnime!

    Title: {anime.title}
    Genre: {anime.genre}
    Year: {anime.year}
    Rating: {anime.rating}

    Watch now: http://127.0.0.1:8000/watch/{anime.id}/

    Enjoy!
    SaiefAnime Team
    """
    
    for user in users:
        if user.email:   # Only send if user has email
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=True,
            )
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

def send_notification_to_all(subject, message):
    """Send email to all registered users"""
    users = User.objects.filter(email__isnull=False).exclude(email='')
    
    success_count = 0
    for user in users:
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=True,
            )
            success_count += 1
        except:
            pass
    
    print(f"✅ Notification sent to {success_count} users.")
    return success_count