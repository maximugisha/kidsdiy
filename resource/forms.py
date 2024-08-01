from django import forms
from .models import Resource, Post, Comment


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['title', 'type', 'audience', 'attachment', 'content', 'categories']


class CreatePostForm(forms.ModelForm):
    attachments = MultipleFileField(label='Select files', required=False)

    class Meta:
        model = Post
        fields = ['audience', 'title', 'content', 'attachments', 'categories']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Add a Comment...'})
        }