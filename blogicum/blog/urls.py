from blog.views import (CategoryPostListView, CommentCreateView,
                        CommentDeleteView, CommentEditView, IndexView,
                        PostCreateView, PostDeleteView, PostDetailView,
                        PostUpdateView, ProfileUpdateView, ProfileView)
from django.urls import path

app_name = 'blog'


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('category/<slug:category_slug>/', CategoryPostListView.as_view(),
         name='category_posts'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='edit_profile'),
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),
    path('posts/create/', PostCreateView.as_view(), name='create_post'),
    path('posts/<int:pk>/edit/', PostUpdateView.as_view(), name='edit_post'),
    path('posts/<int:id>/', PostDetailView.as_view(), name='post_detail'),
    path('posts/<int:id>/delete/', PostDeleteView.as_view(),
         name='delete_post'),
    path('posts/<int:post_id>/comment/', CommentCreateView.as_view(),
         name='add_comment'),
    path('posts/<int:post_id>/edit_comment/<int:id>/',
         CommentEditView.as_view(), name='edit_comment'),
    path('posts/<int:post_id>/delete_comment/<int:id>/',
         CommentDeleteView.as_view(), name='delete_comment'),

]
