from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer


class PostViewSet(viewsets.ModelViewSet):
    """API endpoint for CRUD operations on Posts"""
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class CommentViewSet(viewsets.ModelViewSet):
    """API endpoint for CRUD operations on Comments"""
    queryset = Comment.objects.all().order_by('created_at')
    serializer_class = CommentSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


@api_view(['POST'])
def create_post(request):
    """Create a new post"""
    try:
        content = request.data.get('content', '').strip()
        username = request.data.get('username', 'admin')
        image = request.FILES.get('image', None)
        
        if not content:
            return Response(
                {'error': 'Content is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        post_data = {
            'content': content,
            'username': username
        }
        if image:
            post_data['image'] = image
        
        serializer = PostSerializer(data=post_data, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'message': 'Post created successfully',
                    'post': serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
            
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def get_posts(request):
    """Get all posts with comments"""
    try:
        posts = Post.objects.all().order_by('-created_at')
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(
            {
                'count': posts.count(),
                'posts': serializer.data
            },
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['DELETE'])
def delete_post(request, pk):
    """Delete a post"""
    try:
        post = Post.objects.get(pk=pk)
        post.delete()
        return Response(
            {'message': 'Post deleted successfully'},
            status=status.HTTP_200_OK
        )
    except Post.DoesNotExist:
        return Response(
            {'error': 'Post not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def add_comment(request, post_id):
    """Add a comment to a post"""
    try:
        post = Post.objects.get(pk=post_id)
        content = request.data.get('content', '').strip()
        username = request.data.get('username', 'anonymous')
        
        if not content:
            return Response(
                {'error': 'Comment content is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        comment_data = {
            'post': post.id,
            'content': content,
            'username': username
        }
        
        serializer = CommentSerializer(data=comment_data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'message': 'Comment added successfully',
                    'comment': serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
            
    except Post.DoesNotExist:
        return Response(
            {'error': 'Post not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def get_comments(request, post_id):
    """Get all comments for a post"""
    try:
        post = Post.objects.get(pk=post_id)
        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(
            {
                'count': comments.count(),
                'comments': serializer.data
            },
            status=status.HTTP_200_OK
        )
    except Post.DoesNotExist:
        return Response(
            {'error': 'Post not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )