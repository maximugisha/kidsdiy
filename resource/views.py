# views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from main.models import Organization
from .forms import ResourceForm, CreatePostForm, CommentForm
from .models import Resource, Post, Attachment, Like, DisLike
from main.models import Room, account_info
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, get_object_or_404


def index(request):
    # Retrieve all posts from the database
    posts = Post.objects.all().order_by('-created_at')
    resources = Resource.objects.all().order_by('-created_at')[:3]
    schedules = Room.objects.exclude(room_id__isnull=True).exclude(room_id__exact='')[:5]

    # Get all Organizations
    organizations = Organization.objects.all()

    # Get all Authors
    distinct_authors = Post.objects.values('author').distinct()
    distinct_author_ids = [author['author'] for author in distinct_authors]
    authors = account_info.objects.filter(pk__in=distinct_author_ids)
    # Get the logged-in user (if any) from the request object
    logged_in_user = request.user if request.user.is_authenticated else None
    # Pass posts and logged-in user to the template context
    context = {
        'distinct_author_ids': distinct_author_ids,
        'posts': posts,
        'resources': resources,
        'schedules': schedules,
        'organizations': organizations,
        'authors': authors,
        'logged_in_user': logged_in_user,
        'title': 'Home',
    }

    # Render the HTML template with the context data
    return render(request, 'resource/index.html', context)


# Resources
@login_required(login_url='login')
def create_resource(request):
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES)

        if form.is_valid():
            resource = form.save(commit=False)
            resource.author = account_info.objects.get(user=request.user)
            attached_file = request.FILES.get('attachment')
            attachment = Attachment.objects.create(file=attached_file)
            resource.attachment = attachment
            resource.save()
            categories = form.cleaned_data.get('categories')  # Get selected categories from the form
            resource.categories.set(categories)
            return redirect('home')  # Adjust 'home' to your desired URL name
    else:
        form = ResourceForm()

    return render(request, 'resource/create_resource.html', {'form': form})

@login_required(login_url='login')
def list_resources(request):
    resources = Resource.objects.all()

    context = {
        'resources': resources,
        'title': 'Resource List',
    }

    # Render the HTML template with the context data
    return render(request, 'resource/list.html', context)


def list_posts(request):
    posts = Post.objects.all()

    context = {
        'posts': posts,
        'title': 'Posts List',
    }

    # Render the HTML template with the context data
    return render(request, 'resource/post_list.html', context)


@login_required(login_url='login')
def resource_detail(request, resource_id):
    resource = get_object_or_404(Resource, pk=resource_id)
    return render(request, 'resource/view_resource.html', {'resource': resource})


# Posts
@login_required(login_url='login')
def create_post(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES)
        attachments = request.FILES.getlist('attachments')
        attachment_ids = []
        for attachment in attachments:
            saved_attachment = Attachment.objects.create(file=attachment)
            attachment_ids.append(saved_attachment.id)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = account_info.objects.get(user=request.user)
            post.save()
            # Associate attachments with the post using set()
            post.attachments.set(attachment_ids)
            # Associate categories with the post
            categories = form.cleaned_data.get('categories')  # Get selected categories from the form
            post.categories.set(categories)  # Associate categories with the post
            return redirect('home')
    else:
        form = CreatePostForm()
    return render(request, 'resource/create_post.html', {'form': form, 'title': 'Create Post'})


def post_detail(request, post_id):
    # Your view logic to retrieve the post goes here
    post = Post.objects.get(pk=post_id)

    return render(request, 'resource/view_post.html', {'post': post})

@login_required(login_url='login')
def create_post_comment(request, post_id):
    post = Post.objects.get(pk=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        post = Post.objects.get(pk=post_id)
        if form.is_valid():
            # Create a new comment object but don't save it to the database yet
            comment = form.save(commit=False)
            # Set the current user as the comment's user
            comment.user = account_info.objects.get(user=request.user)
            # Get the post object

            # Set the post for the comment
            comment.post = post
            # Save the comment to the database
            comment.save()
            # Redirect to the post detail page or any other page you want
            return redirect('post_detail', post_id=post_id)
    else:
        form = CommentForm()
    return render(request, 'resource/create_post_comment.html', {'form': form, 'post': post})

@login_required(login_url='login')
def like_post(request, post_id):
    # Get the post object
    post = get_object_or_404(Post, pk=post_id)

    # Check if the user has already liked the post
    if Like.objects.filter(user=account_info.objects.get(user=request.user), post=post).exists():
        # User has already liked the post, handle accordingly
        messages.warning(request, 'You have already liked this post.')
    else:
        # User has not liked the post yet, create a new Like instance
        like = Like(user=account_info.objects.get(user=request.user), post=post)
        like.save()
        messages.success(request, 'You liked the post.')

    # Redirect back to the post detail page

    return redirect('post_detail', post_id=post_id)

@login_required(login_url='login')
def dislike_post(request, post_id):
    # Get the post object
    post = get_object_or_404(Post, pk=post_id)

    # Check if the user has already liked the post
    if DisLike.objects.filter(user=account_info.objects.get(user=request.user), post=post).exists():
        # User has already liked the post, handle accordingly
        messages.warning(request, 'You have already disliked this post.')
    else:
        # User has not liked the post yet, create a new Like instance
        dislike = DisLike(user=account_info.objects.get(user=request.user), post=post)
        dislike.save()
        messages.success(request, 'You Disliked the post.')

    # Redirect back to the post detail page

    return redirect('post_detail', post_id=post_id)
