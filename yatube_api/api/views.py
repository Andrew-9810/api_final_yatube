from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404

from api.serializers import PostSerializer, GroupSerializer, CommentSerializer, FollowSerializer
from api.permission import IsOwnerOrReadOnly
from posts.models import Group, Post, Follow


class PostViewSet(viewsets.ModelViewSet):
    """Класс-представления для обработки данных поста."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    #permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)
    permission_classes = (IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Класс-представления для обработки данных группы."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """Класс-представления для обработки данных комментария."""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)

    def get_queryset(self):
        post_id = self.kwargs.get("post_id")
        post = get_object_or_404(Post, id=post_id)
        return post.comments.all()

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs.get("post_id"))
        serializer.save(author=self.request.user, post=post)


class FollowViewSet(viewsets.ReadOnlyModelViewSet):
    """Класс-представления для обработки данных подписчиков."""
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated, )
