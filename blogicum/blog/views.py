from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.timezone import now
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from blog.models import Category, Comment, Post

from .forms import CommentForm, PostForm, UserProfileForm


class MyLoginRequiredMixin(LoginRequiredMixin):
    login_url = '/auth/login/'
    redirect_field_name = 'next'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:profile', kwargs={
            'username': self.request.user.username})

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user


class PostUpdateView(MyLoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'id': self.object.id})

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if not form:
            raise ValueError("Form class is None or invalid.")
        return form

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user

    def handle_no_permission(self):
        post = self.get_object()
        return redirect('blog:post_detail', id=post.id)


class PostDeleteView(MyLoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/create.html'
    context_object_name = 'post'

    def get_success_url(self):
        return reverse_lazy('blog:index')

    def get_object(self, queryset=None):
        return get_object_or_404(Post, id=self.kwargs['id'])

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user


class ProfileView(ListView):
    model = Post
    template_name = 'blog/profile.html'
    context_object_name = 'page_obj'
    paginate_by = 10

    def get_queryset(self):
        username = self.kwargs.get('username')
        user = get_object_or_404(User, username=username)
        return (
            Post.objects.filter(author=user)
            .annotate(comment_count=Count("comments"))
            .order_by('-pub_date')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(
            User, username=self.kwargs.get('username'))
        context['now'] = now()
        return context


class CategoryPostListView(ListView):
    model = Post
    template_name = 'blog/category.html'
    context_object_name = 'post_list'
    paginate_by = 10

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        category = get_object_or_404(Category, slug=category_slug,
                                     is_published=True)

        return (
            category.posts.select_related('author', 'category', 'location')
            .filter(
                is_published=True,
                pub_date__lte=timezone.now()
            )
            .annotate(comment_count=Count("comments"))
            .order_by('-pub_date')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(
            Category,
            slug=self.kwargs.get('category_slug'))
        return context


class ProfileUpdateView(MyLoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'blog/user.html'

    def get_object(self):
        return self.request.user

    def test_func(self):
        return self.get_object() == self.request.user

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
                pub_date__lte=timezone.now(),
                category__is_published=True,
            )
            .annotate(comment_count=Count("comments"))
            .order_by('-pub_date')
        )


class PostDetailView(MyLoginRequiredMixin, DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        post = get_object_or_404(
            Post.objects.select_related('author', 'category', 'location'),
            id=self.kwargs['id']
        )

        if not (post.category.is_published
                and post.is_published
                and post.pub_date <= timezone.now()):
            if post.author != self.request.user:
                raise Http404("Post not found")

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


class CommentEditView(MyLoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={
            'id': self.object.post.id})

    def get_object(self, queryset=None):
        return get_object_or_404(Comment, id=self.kwargs['id'])

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author


class CommentDeleteView(MyLoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment.html'
    context_object_name = 'comment'

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={
            'id': self.object.post.id})

    def get_object(self, queryset=None):
        return get_object_or_404(Comment, id=self.kwargs['id'])

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author
