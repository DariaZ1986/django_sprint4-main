from django.urls import path

from . import views

app_name = 'blog'


urlpatterns = [
    path('', views.index, name='index'),
    path('category/<slug:category_slug>/', views.category_posts,
         name='category_posts'),
    path('posts/<int:id>/', views.post_detail, name='post_detail'),
    path('posts/<int:id>/delete/',, name='post_delete'),
    path('posts/<int:id>/delete_comment/<int:id>/',,name='comment_delete'),
    path('posts/<int:id>/comment/',,name='comment_add'),
    path('posts/<int:id>/edit_comment/<int:id>/',,name='comment_edit'),
    
]
