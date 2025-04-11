# accounts/views.py
import os

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from .forms import OrganizationForm, UserLoginForm, UserRegisterForm, UserUpdateForm
from .models import Follow, Organization, User


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect("home")
    else:
        form = UserRegisterForm()
    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Logged in successfully!")
                return redirect("home")
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = UserLoginForm()
    return render(request, "accounts/login.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("login")


@login_required
def profile(request, username=None):
    if username is None:
        user = request.user
    else:
        user = get_object_or_404(User, username=username)

    is_following = False
    if request.user.is_authenticated and user != request.user:
        is_following = Follow.objects.filter(
            follower=request.user, following=user
        ).exists()

    context = {
        "profile_user": user,
        "is_following": is_following,
    }
    return render(request, "accounts/profile.html", context)


@login_required
def update_profile(request):
    # Add debugging
    print(f"User is authenticated: {request.user.is_authenticated}")
    print(f"Current user: {request.user.username}")

    if request.method == "POST":
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("profile")
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, "accounts/update_profile.html", {"form": form})

@login_required
def follow_toggle(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)

    if user_to_follow == request.user:
        messages.error(request, "You cannot follow yourself.")
        return redirect("profile", username=user_to_follow.username)

    follow_exists = Follow.objects.filter(
        follower=request.user, following=user_to_follow
    ).exists()

    if follow_exists:
        Follow.objects.filter(follower=request.user, following=user_to_follow).delete()
        messages.success(request, f"You unfollowed {user_to_follow.username}.")
    else:
        Follow.objects.create(follower=request.user, following=user_to_follow)
        messages.success(request, f"You are now following {user_to_follow.username}.")

    return redirect("profile", username=user_to_follow.username)


class CreateSuperUserView(View):
    def get(self, request, *args, **kwargs):
        User = get_user_model()
        username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin')
        email = os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
        password = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'UPbeat123')

        if not User.objects.filter(username=username).exists() and not User.objects.filter(email=email).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            return JsonResponse({'status': 'Superuser created successfully'})
        else:
            return JsonResponse({'status': 'User with this username or email already exists'})
