from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from post_app.models import User, Post, Comment
from post_app.serializers import UserSerializer, PostSerializer, CommentSerializer

from .permissions import PermissionPolicyMixin


# class UserViewSet(ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#
# class PostViewSet(ModelViewSet):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#
#
# class CommentViewSet(ModelViewSet):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer

class UserViewSet(PermissionPolicyMixin, ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes_per_method = {
        'list': [IsAdminUser, IsAuthenticated],
        'create': [AllowAny],
        'update': [IsAdminUser, IsAuthenticated],
        'destroy': [IsAdminUser],
        'retrieve': [IsAdminUser]
    }


class PostViewSet(PermissionPolicyMixin, ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes_per_method = {
        'list': [AllowAny],
        'create': [IsAuthenticated],
        'update': [IsAdminUser, IsAuthenticated],
        'destroy': [IsAdminUser, IsAuthenticated],
        'retrieve': [IsAdminUser]
    }


class CommentViewSet(PermissionPolicyMixin, ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes_per_method = {
        'list': [AllowAny],
        'create': [IsAuthenticated],
        'update': [IsAdminUser],
        'destroy': [IsAdminUser, IsAuthenticated],
        'retrieve': [IsAdminUser, IsAuthenticated]
    }
