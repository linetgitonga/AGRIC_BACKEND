# accounts/views.py
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView
from django.contrib.auth import get_user_model
from .serializers import (
    RegisterSerializer, UserSerializer,
    FarmerProfileSerializer, BuyerProfileSerializer
)
from .models import FarmerProfile, BuyerProfile

User = get_user_model()

class RegisterView(APIView):
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

class FarmerProfileView(RetrieveUpdateAPIView):
    serializer_class = FarmerProfileSerializer
    
    def get_object(self):
        return FarmerProfile.objects.get(user=self.request.user)

class BuyerProfileView(RetrieveUpdateAPIView):
    serializer_class = BuyerProfileSerializer
    
    def get_object(self):
        return BuyerProfile.objects.get(user=self.request.user)