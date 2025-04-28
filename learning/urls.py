from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CourseViewSet, ModuleViewSet, LessonViewSet,
    WebinarViewSet, ResourceViewSet
)

router = DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'modules', ModuleViewSet)
router.register(r'lessons', LessonViewSet)
router.register(r'webinars', WebinarViewSet)
router.register(r'resources', ResourceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]