from django.urls import path

from . import views

urlpatterns = [
    path('video_feed_1/', views.video_feed_1, name="video-feed-1"),
    path('', views.index, name='home'),
]
