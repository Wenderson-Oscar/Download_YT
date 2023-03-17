from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('downloads/music/', views.downloads_music, name='music'),
    path('downloads/video/', views.downloads_video, name='video'),
]