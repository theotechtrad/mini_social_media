from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, Comment


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment model"""
    user = UserSerializer(read_only=True)
    username = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = Comment
        fields = ['id', 'post', 'user', 'username', 'content', 'created_at']
        read_only_fields = ['id', 'created_at', 'user']
    
    def create(self, validated_data):
        username = validated_data.pop('username', None)
        if username:
            user, created = User.objects.get_or_create(username=username)
            validated_data['user'] = user
        return super().create(validated_data)


class PostSerializer(serializers.ModelSerializer):
    """Serializer for Post model"""
    user = UserSerializer(read_only=True)
    username = serializers.CharField(write_only=True, required=False)
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()
    image = serializers.ImageField(required=False, allow_null=True)
    
    class Meta:
        model = Post
        fields = ['id', 'user', 'username', 'content', 'image', 'comments', 
                  'comments_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'user', 'comments', 'comments_count']
    
    def get_comments_count(self, obj):
        return obj.comments.count()
    
    def create(self, validated_data):
        username = validated_data.pop('username', 'admin')
        user, created = User.objects.get_or_create(username=username)
        validated_data['user'] = user
        return super().create(validated_data)
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        if instance.image:
            request = self.context.get('request')
            if request:
                representation['image'] = request.build_absolute_uri(instance.image.url)
            else:
                representation['image'] = instance.image.url
        else:
            representation['image'] = None
            
        return representation