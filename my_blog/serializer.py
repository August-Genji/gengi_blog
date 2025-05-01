from rest_framework import serializers
from .models import Comment, Post, Like, Favorite, Profile, PostWorkFlow
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']


class PostSeriliazer(serializers.ModelSerializer):
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    author = serializers.CharField(source='author.username', read_only=True)
    likes = serializers.SerializerMethodField()
    favorites = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'content', 'created_date', 'comments', 'likes', 'favorites',]
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

    def get_likes(self, obg):
        return obg.likes.count()

    def get_favorites(self, obg):
        return obg.favorites.count()

class PostWorkFlowSerializer(serializers.ModelSerializer):
    post_title = serializers.CharField(source='post.title', read_only=True)

    class Meta:
        model = PostWorkFlow
        fields = ['post_title', 'step', 'note', 'timestamp']


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

    def get_post(self, obj):
        return obj.post.title

    def get_author(self, obj):
        return obj.author.username


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']


class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'user', 'post', 'added_at']

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Profile
        fields = ['id', 'avatar', 'user']
