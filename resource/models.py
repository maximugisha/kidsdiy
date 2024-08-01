import os
from django.db import models
from main.models import BaseModel, account_info
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.contrib.auth.models import User
# import magic


# Create your models here.


class Audience(BaseModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = getattr(settings, 'ALLOWED_EXTENSIONS', ['.mp4', '.zip', '.jpeg', '.jpg', '.png', '.py', '.ino', '.txt'])
    if not ext.lower() in valid_extensions:
        raise ValidationError(_('Unsupported file extension.'))


def validate_file_size(value):
    max_size = getattr(settings, 'MAX_UPLOAD_SIZE', 2 * 1024 * 1024)  # 2 MB
    if value.size > max_size:
        raise ValidationError(_('File size exceeds the maximum allowed size.'))


# TODO ACTIVATE THIS
# def validate_file_content(value):
#     file_type = magic.from_buffer(value.read(), mime=True)
#     allowed_mime_types = getattr(settings, 'ALLOWED_MIME_TYPES', ['image/jpeg', 'image/png', 'video/mp4',
#                                                                   'text/plain', 'text/x-python', 'application/zip'])
#     if file_type not in allowed_mime_types:
#         raise ValidationError(_('Invalid file type.'))


def get_file_extension(filename):
    return os.path.splitext(filename)[1]


class Attachment(models.Model):
    file = models.FileField(upload_to='attachments', validators=[
        validate_file_extension, validate_file_size])  # add this back validate_file_content
    file_name = models.CharField(max_length=255)
    file_size = models.IntegerField()  # Store file size in bytes
    file_extension = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.file_name}{self.file_extension}'

    def save(self, *args, **kwargs):
        self.file_name = self.file.name
        self.file_size = self.file.size
        self.file_extension = get_file_extension(self.file_name)
        super(Attachment, self).save(*args, **kwargs)


class ResourceType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Resource(BaseModel):
    title = models.CharField(max_length=255, null=True, blank=True)
    type = models.ForeignKey(ResourceType, on_delete=models.CASCADE, null=True, blank=True)
    author = models.ForeignKey(account_info, on_delete=models.CASCADE, related_name='resource_author')
    content = models.TextField(null=True, blank=True)
    attachment = models.ForeignKey('Attachment', related_name='resource_files', blank=True, on_delete=models.CASCADE, null=True)
    categories = models.ManyToManyField('main.Interest', related_name='resource_categories', blank=True)
    audience = models.ForeignKey(Audience, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} - {self.author.username}'


class Post(BaseModel):
    title = models.CharField(max_length=255, null=True, blank=True)
    author = models.ForeignKey(account_info, on_delete=models.CASCADE, related_name='post_author')
    content = models.TextField()
    attachments = models.ManyToManyField('Attachment', related_name='post_attachments', blank=True)
    categories = models.ManyToManyField('main.Interest', related_name='post_categories', blank=True)
    audience = models.ForeignKey(Audience, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_likes_count(self):
        return self.likes.count()  # Count the number of likes associated with this resource

    def get_dislikes_count(self):
        return self.dislikes.count()

    def get_comments_count(self):
        return self.post_comments.count()  # Count the number of likes associated with this resource


class Like(BaseModel):
    user = models.ForeignKey(account_info, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ('user', 'post')


class DisLike(BaseModel):
    user = models.ForeignKey(account_info, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='dislikes')

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ('user', 'post')


class Comment(BaseModel):
    user = models.ForeignKey(account_info, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')
    content = models.TextField()

    def __str__(self):
        return self.content

    class Meta:
        ordering = ['-created_at']
