from django.urls import path

from blog.views import IndexView

from . import views

app_name = 'blog'


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('category/<slug:category_slug>/', views.category_posts,
         name='category_posts'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('posts/create/', views.create_post, name='create_post'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('posts/<int:post_id>/delete/', views.post_delete, name='post_delete'),
    path('posts/<int:post_id>/delete_comment/<int:comment_id>/',
         views.comment_delete, name='comment_delete'),
    path('posts/<int:post_id>/comment/', views.comment_add,
         name='comment_add'),
    path('posts/<int:post_id>/edit_comment/<int:comment_id>/',
         views.comment_edit, name='comment_edit'),
     
]
