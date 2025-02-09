from datetime import datetime

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.timezone import now
from django.http import Http404, HttpResponseForbidden
from django.views.generic import (CreateView, ListView, UpdateView,
                                  DetailView, DeleteView)

from blog.models import Category, Post, Comment
from .forms import PostForm, UserProfileForm, CommentForm


class MyLoginRequiredMixin(LoginRequiredMixin):
    login_url = '/auth/login/'
    redirect_field_name = 'next'


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'id': self.object.id})


class PostUpdateView(MyLoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'id': self.object.id})


class PostDeleteView(MyLoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/create.html'
    context_object_name = 'post'

    def get_success_url(self):
        return reverse_lazy('blog:index')

    def get_object(self, queryset=None):
        return get_object_or_404(Post, id=self.kwargs['id'])


class ProfileView(MyLoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/profile.html'
    context_object_name = 'page_obj'
    paginate_by = 10

    def get_queryset(self):
        username = self.kwargs.get('username')
        user = get_object_or_404(User, username=username)
        return Post.objects.filter(author=user).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(
            User, username=self.kwargs.get('username'))
        context['now'] = now()
        return context


class CategoryPostsView(ListView):
    model = Post
    template_name = 'blog/category.html'
    context_object_name = 'post_list'
    paginate_by = 10

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        try:
            category = get_object_or_404(Category, slug=category_slug, is_published=True)
        except Http404:
            raise Http404("Категория не найдена или она не опубликована")

        post_list = Post.objects.filter(
            category=category,
            is_published=True,
            pub_date__lte=datetime.now(),
            category__is_published=True
        ).order_by('-pub_date')

        if not post_list.exists():
            # Если посты не найдены, можно вернуть пустой список
            return post_list

        return post_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs['category_slug']
        try:
            category = get_object_or_404(Category, slug=category_slug)
        except Http404:
            raise Http404("Категория не найдена.")
        
        context['category'] = category
        return context


class ProfileUpdateView(MyLoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'blog/user.html'
    context_object_name = 'profile'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('blog:profile',
                            kwargs={'username': self.request.user.username})


class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 10

    def get_queryset(self):
        return (
            Post.objects.select_related('author', 'category', 'location')
            .filter(
                is_published=True,
                pub_date__lte=datetime.now(),
                category__is_published=True,
            )
            .order_by('-pub_date')
        )


class PostDetailView(MyLoginRequiredMixin, DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        post = get_object_or_404(
            Post.objects.select_related('author', 'category', 'location').filter(
                is_published=True,
                pub_date__lte=timezone.now(),
                category__is_published=True
            ),
            id=self.kwargs['id']
        )

        # Если доступ запрещен, возвращаем ошибку
        if not post.is_published:
            raise HttpResponseForbidden("У вас нет доступа к этому посту.")
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comments.all()
        return context


class CommentCreateView(MyLoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'

    def form_valid(self, form):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        form.instance.author = self.request.user
        form.instance.post = post
        form.save()
        return redirect(reverse_lazy('blog:post_detail',
                                     kwargs={'id': post.id}))


class CommentEditView(MyLoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'id': self.object.post.id})

    def get_object(self, queryset=None):
        comment = get_object_or_404(Comment, id=self.kwargs['id'])
        # Проверка, если текущий пользователь не является автором комментария
        if comment.author != self.request.user:
            raise HttpResponseForbidden("Вы не можете редактировать этот комментарий.")
        return comment


class CommentDeleteView(MyLoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment.html'
    context_object_name = 'comment'

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'id': self.object.post.id})

    def get_object(self, queryset=None):
        comment = get_object_or_404(Comment, id=self.kwargs['id'])
        # Проверка, если текущий пользователь не является автором комментария
        if comment.author != self.request.user:
            raise HttpResponseForbidden("Вы не можете удалить этот комментарий.")
        return comment
