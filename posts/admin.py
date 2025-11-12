from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Admin interface for Post model"""
    list_display = ['id', 'user', 'content_preview', 'has_image', 'comments_count', 'created_at']
    list_filter = ['created_at', 'user']
    search_fields = ['content', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Post Information', {
            'fields': ('user', 'content', 'image')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'
    
    def has_image(self, obj):
        return '✓' if obj.image else '✗'
    has_image.short_description = 'Image'
    has_image.boolean = True
    
    def comments_count(self, obj):
        return obj.comments.count()
    comments_count.short_description = 'Comments'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin interface for Comment model"""
    list_display = ['id', 'user', 'post', 'content_preview', 'created_at']
    list_filter = ['created_at', 'user']
    search_fields = ['content', 'user__username', 'post__content']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Comment Information', {
            'fields': ('post', 'user', 'content')
        }),
        ('Timestamp', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'