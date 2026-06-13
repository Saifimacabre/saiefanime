from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('home/', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('watch/<int:anime_id>/', views.watch, name='watch'),
    
    # New Pages
    path('series/', views.series, name='series'),
    path('movies/', views.movies, name='movies'),
    path('new/', views.new_popular, name='new_popular'),
    path('mylist/', views.my_list, name='my_list'),
    path('search/', views.search, name='search'),
]