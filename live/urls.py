from django.urls import path
from .views import video_conference

urlpatterns = [
    path('', video_conference, name='live'),
    # Other URL patterns
]
