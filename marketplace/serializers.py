# marketplace/serializers.py
from rest_framework import serializers
from .models import Product, ProductImage, Order, OrderItem, Review
from crops.serializers import CropSerializer
from accounts.serializers import UserSerializer
import uuid

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('id', 'image', 'is_primary')

class ProductSerializer(serializers.ModelSerializer):
    seller = UserSerializer(read_only=True)
    crop_details = CropSerializer(source='crop', read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('seller', 'created_at', 'updated_at')
    
    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / len(reviews)
        return 0

class ProductCreateSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Product
        exclude = ('seller', 'created_at', 'updated_at')
    
    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        product = Product.objects.create(**validated_data)
        
        for index, image in enumerate(images_data):
            ProductImage.objects.create(
                product=product,
                image=image,
                is_primary=(index == 0)  # First image is primary
            )
        
        return product

class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('user', 'created_at')

class OrderItemSerializer(serializers.ModelSerializer):
    product_details = ProductSerializer(source='product', read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'product_details', 'quantity', 'price_per_unit', 'total_price')
        read_only_fields = ('price_per_unit',)

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    buyer = UserSerializer(read_only=True)
    
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('buyer', 'order_number', 'total_amount', 'created_at', 'updated_at')
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        
        # Generate a unique order number
        order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        
        # Create order
        order = Order.objects.create(
            order_number=order_number,
            **validated_data
        )
        
        # Create order items and calculate total
        total_amount = 0
        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']
            
            # Check if sufficient quantity is available
            if product.quantity_available < quantity:
                raise serializers.ValidationError(f"Insufficient quantity available for {product.title}")
            
            # Create order item
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price_per_unit=product.price_per_unit
            )
            
            # Update total amount
            total_amount += quantity * product.price_per_unit
            
            # Update product quantity
            product.quantity_available -= quantity
            if product.quantity_available <= 0:
                product.status = 'sold'
            product.save()
        
        # Update order total
        order.total_amount = total_amount + order.shipping_cost
        order.save()
        
        return order