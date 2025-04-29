from rest_framework import serializers
from .models import Comment, Post
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']


class PostSeriliazer(serializers.ModelSerializer):
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    author = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'content', 'created_date', 'comments']
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