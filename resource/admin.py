from django.contrib import admin
from .models import Audience, Attachment, Resource, Like, Comment, ResourceType, Post


# Register your models here.

@admin.register(Audience)
class AudienceAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ['file_name', 'file_size', 'file_extension']
    readonly_fields = ['file_name', 'file_size', 'file_extension']


@admin.register(ResourceType)
class ResourceTypeAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'content']


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    def short_content(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content

    short_content.short_description = 'Short Content'
    list_display = ['author', 'short_content', 'audience']
    # filter_horizontal = ['attachment']


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'post']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    def short_content(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content

    short_content.short_description = 'Short Content'
    list_display = ['user', 'post', 'short_content']
