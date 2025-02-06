from datetime import datetime

from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView

from blog.models import Category, Post


def get_filtered_posts(queryset):
    return (
        queryset.select_related('author', 'category', 'location')
        .filter(
            is_published=True,
            pub_date__lte=datetime.now(),
            category__is_published=True,
        )
    )


class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 10  # Пагинация на 10 постов

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


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True)
    post_list = get_filtered_posts(category.posts.all())
    context = {
        'category': category,
        'post_list': post_list,
    }
    return render(request, template, context)


def post_detail(request, id):
    template = 'blog/detail.html'
    post = get_object_or_404(get_filtered_posts(Post.objects.all()), id=id)
    context = {'post': post}
    return render(request, template, context)


def post_delete(request):
    pass


def comment_add(request):
    pass


def comment_edit(request):
    pass


def comment_delete(request):
    pass


def create_post(request):
    pass


def profile(request):
    pass


def registration(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/login.html',
                  {'form': form, 'registration': True})