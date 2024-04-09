from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import Post

class CreatePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        title = request.data.get('title')
        content = request.data.get('content')
        board = request.data.get('board', 'General')
        upvotes = request.data.get('upvotes', 0)
        downvotes = request.data.get('downvotes', 0)

        if not title or not content:
            return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

        post = Post.objects.create(
            title=title,
            content=content,
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
        board = request.data.get('board', post.board)
        upvotes = request.data.get('upvotes', post.upvotes)
        downvotes = request.data.get('downvotes', post.downvotes)

        post.title = title
        post.content = content
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