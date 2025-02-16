from datetime import datetime

from django import forms
from django.contrib.auth.models import User

from .models import Comment, Post


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('author',)

    def clean_publish_date(self):
        publish_date = self.cleaned_data.get('pub_date')
        if publish_date and publish_date < datetime.now():
            raise forms.ValidationError(
                'Дата публикации не может быть в прошлом!')
        return publish_date


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(
                attrs={'rows': 3,
                       'class': 'form-control',
                       'placeholder': 'Напишите комментарий...'})
        }
