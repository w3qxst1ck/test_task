from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.models import Post
from .models import Comment
from posts.utils import create_comments_tree
from .serializers import CreateCommentModelSerializer, UpdateCommentModelSerializer


class CommentsListView(APIView):
    def get(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        comments = post.comments.all()
        result = create_comments_tree(comments)
        return Response({'comments': result})


class CreateCommentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = CreateCommentModelSerializer(data=request.data)
        if serializer.is_valid():
            # chek if parent in request
            if serializer.data.get('parent'):
                # get post
                try:
                    post = Post.objects.get(id=serializer.data['post'])
                except Post.DoesNotExist:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                try:
                    # get parent and check its in that post
                    parent = Comment.objects.get(id=serializer.data['parent'])
                    post_comments = post.comments.all()
                    if parent not in post_comments:
                        return Response(status=status.HTTP_400_BAD_REQUEST)
                    comment = Comment.objects.create(
                        post=post,
                        user=request.user,
                        text=serializer.data['text'],
                        is_child=serializer.data['is_child'],
                        parent=parent
                    )
                    comment.save()
                except Comment.DoesNotExist:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            # not parent in request
            else:
                try:
                    post = Post.objects.get(id=serializer.data['post'])
                except Post.DoesNotExist:
                    return Response(status=status.HTTP_400_BAD_REQUEST)

                comment = Comment.objects.create(
                    post=post,
                    user=request.user,
                    text=serializer.data['text'],
                    is_child=serializer.data['is_child']
                )
                comment.save()

            return Response(status=status.HTTP_201_CREATED)


class UpdateCommentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk):
        serializer = UpdateCommentModelSerializer(data=request.data)
        if serializer.is_valid():
            try:
                comment = Comment.objects.get(id=pk)
            except Comment.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            if request.user == comment.user:
                comment.text = serializer.data['text']
                comment.save()
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
            return Response(status=status.HTTP_200_OK)


class DeleteCommentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        try:
            comment = Comment.objects.get(id=pk)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if request.user == comment.user:
            comment.delete()
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return Response(status=status.HTTP_200_OK)








