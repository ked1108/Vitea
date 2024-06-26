from django.http import Http404
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.db.models import Count
from .models import Post, Comment

def get_comment(pk):
    try:
        return Comment.objects.get(pk=pk)
    except Comment.DoesNotExist:
        return None

class CreatePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        title = request.data.get('title')
        content = request.data.get('content')
        description = request.data.get('description')  # Added description field
        board = request.data.get('board', 'General')
        upvotes = request.data.get('upvotes', 0)
        downvotes = request.data.get('downvotes', 0)

        if not title or not content or not description:  # Check if description is provided
            return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

        post = Post.objects.create(
            title=title,
            content=content,
            description=description,  # Added description field
            board=board,
            upvotes=upvotes,
            downvotes=downvotes,
            author=request.user,
            created_at=timezone.now(),
            updated_at=timezone.now()
        )

        return Response({"message": "Post created successfully", "post": {
            "id": post.id,
            "title": post.title,
            "content": str(post.content),
            "description": str(post.description),  # Added description field
            "board": post.board,
            "upvotes": post.upvotes,
            "downvotes": post.downvotes,
            "author": post.author.username,
            "created_at": post.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "updated_at": post.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }}, status=status.HTTP_201_CREATED)

class PostDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        return Response({
            "id": post.id,
            "title": post.title,
            "content": str(post.content),
            "description": str(post.description),  # Added description field
            "board": post.board,
            "upvotes": post.upvotes,
            "downvotes": post.downvotes,
            "author": post.author.username,
            "created_at": post.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "updated_at": post.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        })

    def put(self, request, pk, format=None):
        post = self.get_object(pk)
        title = request.data.get('title', post.title)
        content = request.data.get('content', post.content)
        description = request.data.get('description', post.description)  # Added description field
        board = request.data.get('board', post.board)
        upvotes = request.data.get('upvotes', post.upvotes)
        downvotes = request.data.get('downvotes', post.downvotes)

        post.title = title
        post.content = content
        post.description = description  # Added description field
        post.board = board
        post.upvotes = upvotes
        post.downvotes = downvotes
        post.save()

        return Response({
            "message": "Post updated successfully",
            "post": {
                "id": post.id,
                "title": post.title,
                "content": str(post.content),
                "description": str(post.description),  # Added description field
                "board": post.board,
                "upvotes": post.upvotes,
                "downvotes": post.downvotes,
                "author": post.author.username,
                "created_at": post.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                "updated_at": post.updated_at.strftime('%Y-%m-%d %H:%M:%S')
            }
        }, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        post = self.get_object(pk)
        post.delete()
        return Response({"message": "Post deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    

class CreateCommentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        content = request.data.get('content')
        post_id = request.data.get('post')
        parent_id = request.data.get('parent')
        parent = get_comment(parent_id) if parent_id else None

        if not content or not post_id:
            return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

        comment = Comment.objects.create(
            content=content,
            post_id=post_id,
            author=request.user,
            parent=parent,
            created_at=timezone.now(),
            updated_at=timezone.now()
        )

        return Response({"message": "Comment created successfully", "comment": {
            "id": comment.id,
            "content": comment.content,
            "post": comment.post_id,
            "parent": comment.parent.id if comment.parent else None,
            "author": comment.author.username,
            "created_at": comment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "updated_at": comment.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }}, status=status.HTTP_201_CREATED)


class CommentDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        comment = self.get_object(pk)
        return Response({
            "id": comment.id,
            "content": comment.content,
            "post": comment.post_id,
            "parent": comment.parent.id if comment.parent else None,
            "author": comment.author.username,
            "created_at": comment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "updated_at": comment.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        })

    def put(self, request, pk, format=None):
        comment = self.get_object(pk)
        content = request.data.get('content', comment.content)
        parent_id = request.data.get('parent')
        parent = get_comment(parent_id) if parent_id else None

        comment.content = content
        comment.parent = parent
        comment.save()

        return Response({
            "message": "Comment updated successfully",
            "comment": {
                "id": comment.id,
                "content": comment.content,
                "post": comment.post_id,
                "parent": comment.parent.id if comment.parent else None,
                "author": comment.author.username,
                "created_at": comment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                "updated_at": comment.updated_at.strftime('%Y-%m-%d %H:%M:%S')
            }
        }, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        comment = self.get_object(pk)
        comment.delete()
        return Response({"message": "Comment deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
class BoardPostsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        board = request.query_params.get('board', None)
        if not board:
            return Response({"error": "Missing required query parameter: 'board'"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            posts = Post.objects.filter(board=board)
        except Post.DoesNotExist:
            raise Http404

        posts_data = [{
            "id": post.id,
            "title": post.title,
            "content": str(post.content),
            "description": str(post.description),
            "board": post.board,
            "upvotes": post.upvotes,
            "downvotes": post.downvotes,
            "author": post.author.username,
            "created_at": post.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "updated_at": post.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        } for post in posts]

        return Response(posts_data, status=status.HTTP_200_OK)
    
class TopPostsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        boards = Post.objects.values('board').annotate(total=Count('board')).order_by('-total')

        top_posts = []
        for board in boards:
            posts = Post.objects.filter(board=board['board']).order_by('-upvotes')[:5]
            posts_data = [{
                "id": post.id,
                "title": post.title,
                "content": str(post.content),
                "description": str(post.description),
                "board": post.board,
                "upvotes": post.upvotes,
                "downvotes": post.downvotes,
                "author": post.author.username,
                "created_at": post.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                "updated_at": post.updated_at.strftime('%Y-%m-%d %H:%M:%S')
            } for post in posts]
            top_posts.append({board['board']: posts_data})

        return Response(top_posts, status=status.HTTP_200_OK)
    

class CreateReplyView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        post_id = request.data.get('post_id')
        content = request.data.get('content')

        if not post_id or not content:
            return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

        reply = Comment.objects.create(
            content=content,
            post=post,
            author=request.user,
            created_at=timezone.now(),
            updated_at=timezone.now()
        )

        return Response({"message": "Reply created successfully", "reply": {
            "id": reply.id,
            "content": str(reply.content),
            "post_id": reply.post.id,
            "author": reply.author.username,
            "created_at": reply.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "updated_at": reply.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }}, status=status.HTTP_201_CREATED)