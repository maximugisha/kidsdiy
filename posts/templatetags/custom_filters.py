# custom_filters.py
from django import template

register = template.Library()


@register.filter
def user_liked(post, user):
    return post.likes.filter(user=user).exists()
