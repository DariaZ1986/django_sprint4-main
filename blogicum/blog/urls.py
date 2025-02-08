from django.urls import path

from blog.views import IndexView, PostCreateView, ProfileView

from . import views

app_name = 'blog'


urlpatterns = [
     path('', IndexView.as_view(), name='index'),
     path('category/<slug:category_slug>/', views.category_posts,
          name='category_posts'),
     path('profile/<str:username>/', views.ProfileView.as_view(),
          name='profile'),
     path('posts/create/', PostCreateView.as_view(), name='create_post'),
     path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
     path('posts/<int:post_id>/delete/', views.post_delete, name='post_delete'),
     path('posts/<int:post_id>/delete_comment/<int:comment_id>/',
          views.comment_delete, name='comment_delete'),
     path('posts/<int:post_id>/comment/', views.comment_add,
          name='comment_add'),
     path('posts/<int:post_id>/edit_comment/<int:comment_id>/',
          views.comment_edit, name='comment_edit'),
     path('profile/<str:username>/edit/',
          views.ProfileUpdateView.as_view(), name='edit_profile'),
     
]
