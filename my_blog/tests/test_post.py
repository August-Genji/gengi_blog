import pytest
from my_blog.models import Post
from django.contrib.auth.models import User


@pytest.mark.django_db
class TestPostModel:

    def test_str_method(self):
        user = User.objects.create_user(username="test_user")
        post = Post.objects.create(title="Test Title", content="Test Content", author=user)
        assert str(post) == "Test Title"
