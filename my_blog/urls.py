from rest_framework.urls import path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, PostViewSet, CommentViewSet, LikeViewSet, FavoriteViewSet, ProfileViewSet

router = DefaultRouter()
router.register(r'user', UserViewSet)
router.register(r'post', PostViewSet)
router.register(r'comment', CommentViewSet)
router.register(r'like', LikeViewSet)
router.register(r'favorite', FavoriteViewSet)
router.register(r'profile', ProfileViewSet)

urlpatterns = router.urls
