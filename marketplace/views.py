# marketplace/views.py
from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from .models import Product, Order, Review
from .serializers import (
    ProductSerializer, ProductCreateSerializer, OrderSerializer,
    ReviewSerializer
)

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['crop', 'is_organic', 'status', 'seller']
    search_fields = ['title', 'description', 'location']
    ordering_fields = ['price_per_unit', 'created_at', 'quantity_available']
    
    def get_queryset(self):
        queryset = Product.objects.all()
        
        # Filter by available status for non-owner users
        if self.action == 'list':
            if not self.request.query_params.get('seller'):
                queryset = queryset.filter(status='available')
        
        return queryset
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ProductCreateSerializer
        return ProductSerializer
    
    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)
    
    @action(detail=True, methods=['post'])
    def add_review(self, request, pk=None):
        product = self.get_object()
        serializer = ReviewSerializer(data=request.data)
        
        if serializer.is_valid():
            # Check if user already reviewed this product
            if Review.objects.filter(product=product, user=request.user).exists():
                return Response(
                    {"detail": "You have already reviewed this product."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            serializer.save(product=product, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def my_products(self, request):
        products = Product.objects.filter(seller=request.user)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Buyers see their orders, sellers see orders containing their products
        user = self.request.user
        if user.user_type == 'buyer':
            return Order.objects.filter(buyer=user)
        elif user.user_type == 'farmer':
            # Get orders that contain the farmer's products
            return Order.objects.filter(items__product__seller=user).distinct()
        return Order.objects.none()
    
    def perform_create(self, serializer):
        serializer.save(buyer=self.request.user)
    
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        order = self.get_object()
        status = request.data.get('status')
        
        if not status or status not in dict(Order.STATUS_CHOICES):
            return Response(
                {"detail": "Invalid status value"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if user is allowed to update status
        if request.user != order.buyer and not any(item.product.seller == request.user for item in order.items.all()):
            return Response(
                {"detail": "You don't have permission to update this order's status"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        order.status = status
        order.save()
        
        return Response(OrderSerializer(order).data)

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Review.objects.filter(
            Q(user=self.request.user) | Q(product__seller=self.request.user)
        )
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)