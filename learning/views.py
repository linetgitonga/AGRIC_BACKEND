from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Course, Module, Lesson, Webinar, Resource
from .serializers import (
    CourseSerializer, ModuleSerializer, LessonSerializer,
    WebinarSerializer, ResourceSerializer
)

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_free']
    search_fields = ['title', 'description']

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)

class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['course']

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['module']

class WebinarViewSet(viewsets.ModelViewSet):
    queryset = Webinar.objects.all()
    serializer_class = WebinarSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_free', 'scheduled_time']
    search_fields = ['title', 'description']

    def perform_create(self, serializer):
        serializer.save(speaker=self.request.user)

    @action(detail=True, methods=['post'])
    def register(self, request, pk=None):
        webinar = self.get_object()
        if hasattr(webinar, 'participants'):
            webinar.participants.add(request.user)
            return Response({'status': 'registered for webinar'})
        return Response({'status': 'registration not available'})

class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['resource_type']
    search_fields = ['title', 'description']