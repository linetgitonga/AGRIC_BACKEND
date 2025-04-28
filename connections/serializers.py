# connections/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    ContractRequest, BuyerPreference, FarmerOffer,
    Connection, Message
)
from accounts.serializers import UserSerializer
from crops.serializers import CropSerializer

User = get_user_model()

class ContractRequestSerializer(serializers.ModelSerializer):
    buyer_details = UserSerializer(source='buyer', read_only=True)
    farmer_details = UserSerializer(source='farmer', read_only=True)
    crop_details = CropSerializer(source='crop', read_only=True)
    
    class Meta:
        model = ContractRequest
        fields = '__all__'
        read_only_fields = ('buyer', 'status', 'created_at', 'updated_at')

class BuyerPreferenceSerializer(serializers.ModelSerializer):
    buyer_details = UserSerializer(source='buyer', read_only=True)
    preferred_crops_details = CropSerializer(source='preferred_crops', many=True, read_only=True)
    
    class Meta:
        model = BuyerPreference
        fields = '__all__'
        read_only_fields = ('buyer',)

class FarmerOfferSerializer(serializers.ModelSerializer):
    farmer_details = UserSerializer(source='farmer', read_only=True)
    crop_details = CropSerializer(source='crop', read_only=True)
    
    class Meta:
        model = FarmerOffer
        fields = '__all__'
        read_only_fields = ('farmer', 'created_at', 'updated_at')

class ConnectionSerializer(serializers.ModelSerializer):
    initiator_details = UserSerializer(source='initiator', read_only=True)
    receiver_details = UserSerializer(source='receiver', read_only=True)
    
    class Meta:
        model = Connection
        fields = '__all__'
        read_only_fields = ('initiator', 'created_at', 'updated_at')

class MessageSerializer(serializers.ModelSerializer):
    sender_details = UserSerializer(source='sender', read_only=True)
    receiver_details = UserSerializer(source='receiver', read_only=True)
    
    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ('sender', 'is_read', 'created_at')