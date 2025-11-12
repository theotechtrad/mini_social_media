from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'posts', views.PostViewSet, basename='post')
router.register(r'comments', views.CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
    path('create-post/', views.create_post, name='create-post'),
    path('get-posts/', views.get_posts, name='get-posts'),
    path('delete-post/<int:pk>/', views.delete_post, name='delete-post'),
    path('add-comment/<int:post_id>/', views.add_comment, name='add-comment'),
    path('get-comments/<int:post_id>/', views.get_comments, name='get-comments'),
]