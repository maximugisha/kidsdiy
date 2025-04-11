# accounts/urls.py
from django.urls import path

from . import views
from .views import CreateSuperUserView

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('profile/', views.profile, name='profile'),

    path("follow/<int:user_id>/", views.follow_toggle, name="follow_toggle"),
    path('create-superuser/', CreateSuperUserView.as_view(), name='create_superuser'),
]
