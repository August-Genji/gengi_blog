from rest_framework.urls import path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, PostViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'user', UserViewSet)
router.register(r'post', PostViewSet)
router.register(r'comment', CommentViewSet)

urlpatterns = router.urls
