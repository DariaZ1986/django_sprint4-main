from datetime import datetime

from blog.models import Category, Post
from django.shortcuts import get_object_or_404, render


def get_filtered_posts(queryset):
    return (
        queryset.select_related('author', 'category', 'location')
        .filter(
            is_published=True,
            pub_date__lte=datetime.now(),
            category__is_published=True,
        )
    )


def index(request):
    template = 'blog/index.html'
    post_list = get_filtered_posts(Post.objects)[:5]
    context = {'post_list': post_list}
    return render(request, template, context)


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
