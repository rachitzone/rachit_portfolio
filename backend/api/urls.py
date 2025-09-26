from django.urls import path
from . import views

urlpatterns = [
    path('location-weather/', views.location_weather, name='location-weather'),
    path('spotify/', views.spotify_now_playing, name='spotify-now-playing'),
]
