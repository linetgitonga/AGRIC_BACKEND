# connections/models.py
from django.db import models
from django.contrib.auth import get_user_model
from crops.models import Crop

User = get_user_model()

class ContractRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
        ('fulfilled', 'Fulfilled'),
    )
    
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contract_requests')
    farmer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_contract_requests')
    crop = models.ForeignKey(Crop, on_delete=models.SET_NULL, null=True)
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    quantity_required = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=10)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    
    delivery_date = models.DateField()
    delivery_location = models.CharField(max_length=200)
    
    quality_requirements = models.TextField(blank=True, null=True)
    payment_terms = models.TextField(blank=True, null=True)
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    farmer_notes = models.TextField(blank=True, null=True)
    buyer_notes = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.buyer.email} - {self.crop.name if self.crop else 'Unspecified crop'} - {self.status}"

class BuyerPreference(models.Model):
    buyer = models.OneToOneField(User, on_delete=models.CASCADE, related_name='buyer_preference')
    preferred_crops = models.ManyToManyField(Crop, related_name='interested_buyers', blank=True)
    preferred_regions = models.TextField(blank=True, null=True, help_text="Comma separated list of regions")
    is_organic_preferred = models.BooleanField(default=False)
    quantity_needed_monthly = models.TextField(blank=True, null=True, help_text="Description of monthly quantity needs")
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Preferences for {self.buyer.email}"

class FarmerOffer(models.Model):
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('withdrawn', 'Withdrawn'),
        ('sold', 'Sold'),
    )
    
    farmer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='farmer_offers')
    crop = models.ForeignKey(Crop, on_delete=models.SET_NULL, null=True)
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    quantity_available = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=10)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    is_negotiable = models.BooleanField(default=True)
    
    harvest_date = models.DateField()
    available_from = models.DateField()
    available_until = models.DateField()
    
    is_organic = models.BooleanField(default=False)
    quality_description = models.TextField(blank=True, null=True)
    
    location = models.CharField(max_length=200)
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.farmer.email} - {self.crop.name if self.crop else 'Unspecified crop'} - {self.status}"

class Connection(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )
    
    initiator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='initiated_connections')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_connections')
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    message = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('initiator', 'receiver')
    
    def __str__(self):
        return f"{self.initiator.email} -> {self.receiver.email} ({self.status})"

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    
    subject = models.CharField(max_length=200)
    content = models.TextField()
    
    is_read = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Message from {self.sender.email} to {self.receiver.email}"