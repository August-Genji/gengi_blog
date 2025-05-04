from rest_framework.routers import DefaultRouter

from .views import UserViewSet, PostViewSet, CommentViewSet, LikeViewSet, FavoriteViewSet, ProfileViewSet, PostWorkFlowViewSet

router = DefaultRouter()
router.register(r'user', UserViewSet)
router.register(r'post', PostViewSet)
router.register(r'comment', CommentViewSet)
router.register(r'like', LikeViewSet)
router.register(r'favorite', FavoriteViewSet)
router.register(r'profile', ProfileViewSet)
router.register(r'post_workflow', PostWorkFlowViewSet)

urlpatterns = router.urls
