# connections/views.py
from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.shortcuts import get_object_or_404

from .models import (
    ContractRequest, BuyerPreference, FarmerOffer,
    Connection, Message
)
from .serializers import (
    ContractRequestSerializer, BuyerPreferenceSerializer,
    FarmerOfferSerializer, ConnectionSerializer, MessageSerializer
)

class ContractRequestViewSet(viewsets.ModelViewSet):
    serializer_class = ContractRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'crop']
    search_fields = ['title', 'description']
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'buyer':
            return ContractRequest.objects.filter(buyer=user)
        elif user.user_type == 'farmer':
            return ContractRequest.objects.filter(farmer=user)
        return ContractRequest.objects.all()
    
    def perform_create(self, serializer):
        serializer.save(buyer=self.request.user)
    
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        contract_request = self.get_object()
        new_status = request.data.get('status')
        notes = request.data.get('notes', '')
        
        if not new_status or new_status not in dict(ContractRequest.STATUS_CHOICES):
            return Response(
                {"detail": "Invalid status value"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check permissions based on user type and status change
        user = request.user
        if user.user_type == 'farmer' and user == contract_request.farmer:
            if contract_request.status == 'pending' and new_status in ['accepted', 'rejected']:
                contract_request.farmer_notes = notes
                contract_request.status = new_status
                contract_request.save()
                return Response(ContractRequestSerializer(contract_request).data)
        
        elif user.user_type == 'buyer' and user == contract_request.buyer:
            if new_status in ['cancelled']:
                contract_request.buyer_notes = notes
                contract_request.status = new_status
                contract_request.save()
                return Response(ContractRequestSerializer(contract_request).data)
        
        return Response(
            {"detail": "You don't have permission to update this contract request's status"},
            status=status.HTTP_403_FORBIDDEN
        )

class BuyerPreferenceViewSet(viewsets.ModelViewSet):
    serializer_class = BuyerPreferenceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'farmer':
            # Farmers can view all buyer preferences
            return BuyerPreference.objects.all()
        elif user.user_type == 'buyer':
            # Buyers only see their own preferences
            return BuyerPreference.objects.filter(buyer=user)
        return BuyerPreference.objects.none()
    
    def perform_create(self, serializer):
        serializer.save(buyer=self.request.user)

class FarmerOfferViewSet(viewsets.ModelViewSet):
    serializer_class = FarmerOfferSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'crop', 'is_organic']
    search_fields = ['title', 'description', 'location']
    
    def get_queryset(self):
        return FarmerOffer.objects.filter(status='available')
    
    def perform_create(self, serializer):
        serializer.save(farmer=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_offers(self, request):
        offers = FarmerOffer.objects.filter(farmer=request.user)
        serializer = self.get_serializer(offers, many=True)
        return Response(serializer.data)

class ConnectionViewSet(viewsets.ModelViewSet):
    serializer_class = ConnectionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Connection.objects.filter(
            Q(initiator=user) | Q(receiver=user)
        )
    
    def perform_create(self, serializer):
        serializer.save(initiator=self.request.user)
    
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        connection = self.get_object()
        new_status = request.data.get('status')
        
        if not new_status or new_status not in dict(Connection.STATUS_CHOICES):
            return Response(
                {"detail": "Invalid status value"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Only the receiver can accept/reject connection requests
        if request.user != connection.receiver:
            return Response(
                {"detail": "Only the connection receiver can update the status"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        connection.status = new_status
        connection.save()
        
        return Response(ConnectionSerializer(connection).data)

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(
            Q(sender=user) | Q(receiver=user)
        ).order_by('-created_at')
    
    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
    
    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        message = self.get_object()
        
        if request.user != message.receiver:
            return Response(
                {"detail": "Only the message receiver can mark it as read"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        message.is_read = True
        message.save()
        
        return Response(MessageSerializer(message).data)
    
    @action(detail=False, methods=['get'])
    def inbox(self, request):
        messages = Message.objects.filter(receiver=request.user).order_by('-created_at')
        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def sent(self, request):
        messages = Message.objects.filter(sender=request.user).order_by('-created_at')
        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        count = Message.objects.filter(receiver=request.user, is_read=False).count()
        return Response({"unread_count": count})