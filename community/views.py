# from rest_framework import viewsets, permissions, status
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from django.db.models import Count
# from .models import Topic, Discussion, Comment, FarmingGroup
# from .serializers import (
#     TopicSerializer, DiscussionSerializer,
#     CommentSerializer, FarmingGroupSerializer
# )

# class TopicViewSet(viewsets.ModelViewSet):
#     queryset = Topic.objects.filter(is_active=True)
#     serializer_class = TopicSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# class DiscussionViewSet(viewsets.ModelViewSet):
#     serializer_class = DiscussionSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return Discussion.objects.all().order_by('-created_at')

#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)

#     @action(detail=True, methods=['post'])
#     def upvote(self, request, pk=None):
#         discussion = self.get_object()
#         if request.user in discussion.upvotes.all():
#             discussion.upvotes.remove(request.user)
#         else:
#             discussion.upvotes.add(request.user)
#         return Response({'status': 'success'})

# class CommentViewSet(viewsets.ModelViewSet):
#     serializer_class = CommentSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return Comment.objects.all()

#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)

# class FarmingGroupViewSet(viewsets.ModelViewSet):
#     serializer_class = FarmingGroupSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return FarmingGroup.objects.all()

#     def perform_create(self, serializer):
#         serializer.save(creator=self.request.user)

#     @action(detail=True, methods=['post'])
#     def join(self, request, pk=None):
#         group = self.get_object()
#         if request.user in group.members.all():
#             group.members.remove(request.user)
#             return Response({'status': 'left group'})
#         else:
#             group.members.add(request.user)
#             return Response({'status': 'joined group'})

from rest_framework import viewsets, permissions
from .models import Topic, Discussion, Comment, FarmingGroup
from .serializers import (
    TopicSerializer, 
    DiscussionSerializer,
    CommentSerializer, 
    FarmingGroupSerializer
)

class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.filter(is_active=True)
    serializer_class = TopicSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class DiscussionViewSet(viewsets.ModelViewSet):
    queryset = Discussion.objects.all().order_by('-created_at')
    serializer_class = DiscussionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class FarmingGroupViewSet(viewsets.ModelViewSet):
    queryset = FarmingGroup.objects.all()
    serializer_class = FarmingGroupSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)