from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from .models import Comment, Post, Like, Favorite, Profile, PostWorkFlow
from django.contrib.auth.models import User


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    post = serializers.SerializerMethodField()

    post_id = serializers.PrimaryKeyRelatedField(
        queryset=Post.objects.all(), source='post', write_only=True
    )

    class Meta:
        model = Comment
        fields = ['id', 'author', 'post', 'post_id', 'content', 'created_date']
        read_only_fields = ['created_date']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user

        if 'author' in validated_data:
            if not user.is_staff:
                raise serializers.ValidationError("Only admins can set author manually.")
        else:
            validated_data['author'] = user

        return super().create(validated_data)

    @extend_schema_field(str)
    def get_post(self, obj):
        return obj.post.title

    @extend_schema_field(str)
    def get_author(self, obj):
        return obj.author.username


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']


class PostSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=False, allow_blank=True)
    comments = CommentSerializer(many=True, read_only=True)
    author = serializers.CharField(source='author.username', read_only=True)
    likes = serializers.SerializerMethodField()
    favorites = serializers.SerializerMethodField()
    author_email = serializers.EmailField(source='author.email', read_only=True)
    like_count = serializers.IntegerField(read_only=True)
    favorites_count = serializers.IntegerField(read_only=True)


    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'content', 'created_date',
                  'comments', 'likes', 'favorites', 'author_email', 'like_count', 'favorites_count']
        read_only_fields = ['created_date', 'comments']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user

        if 'author' in validated_data:
            if not user.is_staff:
                raise serializers.ValidationError("Only admins can set the author manually.")
        else:
            validated_data['author'] = user

        return super().create(validated_data)



    @extend_schema_field(int)
    def get_likes(self, obj):
        if hasattr(obj, "likes"):
            return obj.likes.count()
        return 0  # или None, как хочешь

    @extend_schema_field(int)
    def get_favorites(self, obj):
        if hasattr(obj, "favorites"):
            return obj.favorites.count()
        return 0


class PostWorkFlowSerializer(serializers.ModelSerializer):
    post_title = serializers.SerializerMethodField()

    class Meta:
        model = PostWorkFlow
        fields = ['post_title', 'step', 'note', 'timestamp']

    @extend_schema_field(str)
    def get_post_title(self, obj):
        return obj.post.title




class LikeSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']


class FavoriteSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='post.author.username', read_only=True)
    post = serializers.CharField(source='post.title', read_only=True)
    user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'user', 'author', 'post', 'added_at']


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'avatar', 'user']

