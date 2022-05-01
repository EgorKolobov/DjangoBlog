from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    CommentCreateView,
    CommentUpdateView,
    CommentDeleteView,
    CommentReplyView,
    UserPostListView
)
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/addcomment/', CommentCreateView.as_view(), name='comment-create'),
    path('post/<int:pk>/updatecomment/<int:comment_pk>/', CommentUpdateView.as_view(), name='comment-update'),
    path('post/<int:pk>/deletecomment/<int:comment_pk>/', CommentDeleteView.as_view(), name='comment-delete'),
    path('post/<int:pk>/replycomment/<int:comment_pk>/', CommentReplyView.as_view(), name='comment-reply'),
    path('about/', views.about, name='blog-about'),
]
