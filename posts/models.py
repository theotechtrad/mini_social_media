from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Post(models.Model):
    """
    Model for social media posts
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        help_text="User who created this post"
    )
    content = models.TextField(
        help_text="Post content/caption"
    )
    image = models.ImageField(
        upload_to='posts/',
        blank=True,
        null=True,
        help_text="Optional image for the post"
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        help_text="When the post was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="When the post was last updated"
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
    
    def __str__(self):
        return f"{self.user.username} - Post {self.id} - {self.content[:50]}..."


class Comment(models.Model):
    """
    Model for comments on posts
    """
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        help_text="Post this comment belongs to"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        help_text="User who wrote this comment"
    )
    content = models.TextField(
        help_text="Comment content"
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        help_text="When the comment was created"
    )
    
    class Meta:
        ordering = ['created_at']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
    
    def __str__(self):
        return f"{self.user.username} commented on Post {self.post.id}"