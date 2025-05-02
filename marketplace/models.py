# marketplace/models.py
from django.db import models
from django.contrib.auth import get_user_model
from crops.models import Crop

User = get_user_model()

class Product(models.Model):
    UNIT_CHOICES = (
        ('kg', 'Kilogram'),
        ('g', 'Gram'),
        ('lb', 'Pound'),
        ('ton', 'Ton'),
        ('piece', 'Piece'),
        ('bunch', 'Bunch'),
        ('dozen', 'Dozen'),
        ('crate', 'Crate'),
        ('bag', 'Bag'),
    )
    
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('sold', 'Sold'),
        ('reserved', 'Reserved'),
        ('unavailable', 'Unavailable'),
    )
    
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    crop = models.ForeignKey(Crop, on_delete=models.SET_NULL, null=True, related_name='products')
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default='kg')
    quantity_available = models.DecimalField(max_digits=10, decimal_places=2)
    
    harvest_date = models.DateField(blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    
    is_organic = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='available')
    
    location = models.CharField(max_length=200, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)




# ADDED FIELDS

    PACKAGING_CHOICES = (
        ('plastic', 'Plastic'),
        ('mesh', 'Mesh Bag'),
        ('carton', 'Carton Box'),
        ('none', 'No Packaging')
    )

    CERTIFICATION_CHOICES = (
        ('None', 'No Certification'),
        ('Organic', 'Organic Certified'),
        ('GAP', 'Good Agricultural Practices'),
        ('Fairtrade', 'Fairtrade Certified')
    )
    
    min_order_quantity = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=1,
        help_text="Minimum quantity that can be ordered"
    )
    
    packaging = models.CharField(
        max_length=20,
        choices=PACKAGING_CHOICES,
        default='none',
        help_text="Type of packaging used"
    )
    
    certification = models.CharField(
        max_length=50,
        choices=CERTIFICATION_CHOICES,
        default='None',
        help_text="Product certification type"
    )
    
    delivery_available = models.BooleanField(
        default=False,
        help_text="Whether delivery service is available"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    is_primary = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Image for {self.product.title}"

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    
    PAYMENT_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    )
    
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_number = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    
    shipping_address = models.TextField()
    shipping_city = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=100)
    shipping_zip = models.CharField(max_length=20)
    shipping_country = models.CharField(max_length=100, default='Kenya')
    
    contact_phone = models.CharField(max_length=20)
    contact_email = models.EmailField()
    
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    notes = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.order_number
    
    class Meta:
        ordering = ['-created_at']

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.title} for order {self.order.order_number}"
    
    @property
    def total_price(self):
        return self.quantity * self.price_per_unit

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.email}'s review of {self.product.title}"
    
    class Meta:
        unique_together = ('product', 'user')