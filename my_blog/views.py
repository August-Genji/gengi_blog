import requests
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.types import OpenApiTypes
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters
from django.http import HttpResponse
import csv
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from .filters import PostWorkFlowFilter, PostFilter
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
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    fiterset_class = PostFilter
    search_fields = ['title', 'content', 'author__username']
    ordering_fields = ['created_date', 'update_date', 'like_count', 'favorites_count', 'author__username']

    @extend_schema(summary="Экспорт постов в csv или json", description=(
            "Экспортируем список посотов с полями : id, title, author_name" "like_count, favorites_count, created_date.\n\n"
            "**Формат:**?format=json или ?format=csv"
    ), responses={200: OpenApiTypes.BINARY})
    @action(detail=False, methods=['get'], url_path='export')
    def export(self, request, *args):
        export_format = self.request.query_params.get('format', 'json')

        queryset = self.get_queryset()
        data = queryset.values('id', 'title', 'author__username', 'like_count', 'favorites_count', 'created_date')

        if export_format == 'csv':
            http_response = HttpResponse(content_type='text/csv')
            http_response['Content-Disposition'] = 'attachment; filename="posts.cvs"'
            writer = csv.DictWriter(http_response, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
            return http_response
        elif export_format == 'json':
            return Response(list(data))

        return Response({'error': 'Unsupported format'}, status=400)
    def get_queryset(self):
        return Post.objects.annotate(like_count=Count('likes'), favorites_count=Count('favorites')).all()

    def perform_create(self, serializer):
        title = serializer.validated_data.get('title')
        description = serializer.validated_data.get('description')

        instance = serializer.save(author=self.request.user)

        if not instance.content:
            webhook_url = "https://hook.eu2.make.com/..."
            requests.post(webhook_url, json={
                "id": instance.id,
                "title": instance.title
            })
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
