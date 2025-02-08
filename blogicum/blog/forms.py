from datetime import datetime

from django import forms
from django.contrib.auth.models import User

from .models import Post


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'category', 'location', 'pub_date']

    def clean_publish_date(self):
        publish_date = self.cleaned_data.get('publish_date')
        if publish_date and publish_date < datetime.now():
            raise forms.ValidationError(
                'Дата публикации не может быть в прошлом!')
        return publish_date
