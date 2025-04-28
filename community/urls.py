from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TopicViewSet,
    DiscussionViewSet,
    CommentViewSet,
    FarmingGroupViewSet
)

router = DefaultRouter()

# Register viewsets with the router
router.register(r'topics', TopicViewSet)
router.register(r'discussions', DiscussionViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'groups', FarmingGroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
]