from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from .filters import PostWorkFlowFilter
from .permissions import IsOwnerOrReadOnly
from .models import Comment, Post, Like, Favorite, Profile, PostWorkFlow
from .serializer import CommentSerializer, PostSerializer, CustomUserSerializer, LikeSerializer, FavoriteSerializer, \
    ProfileSerializer, PostWorkFlowSerializer
from django.contrib.auth.models import User


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_context(self):
        return {'request': self.request}



class PostWorkFlowViewSet(ModelViewSet):
    queryset = PostWorkFlow.objects.all().order_by('-timestamp')
    serializer_class = PostWorkFlowSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_class = PostWorkFlowFilter


class LikeViewSet(ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FavoriteViewSet(ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(oser=self.request.user)
