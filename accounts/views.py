# accounts/views.py
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView
from django.contrib.auth import get_user_model
from .serializers import (
    RegisterSerializer, UserSerializer,LoginSerializer,
    FarmerProfileSerializer, BuyerProfileSerializer
)
from .models import FarmerProfile, BuyerProfile
from django.db import transaction 
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate



User = get_user_model()


class RegisterView(APIView):

    permission_classes = [permissions.AllowAny]
    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
        
        try:
            with transaction.atomic():
                if user_serializer.is_valid():
                    user = user_serializer.save()
                    
                    user_type = request.data.get('user_type')
                    
                    if user_type == 'farmer':
                        # Check if profile already exists
                        if not FarmerProfile.objects.filter(user=user).exists():
                            FarmerProfile.objects.create(user=user)
                    elif user_type == 'buyer':
                        if not BuyerProfile.objects.filter(user=user).exists():
                            BuyerProfile.objects.create(user=user)
                    
                    return Response({
                        'user': user_serializer.data,
                        'message': f'Successfully registered as {user_type}'
                    }, status=status.HTTP_201_CREATED)
                    
                return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            # If any error occurs, rollback the transaction
            return Response({
                'error': str(e),
                'message': 'Registration failed'
            }, status=status.HTTP_400_BAD_REQUEST)


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






class LoginView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            user = authenticate(email=email, password=password)
            
            if user is not None:
                # Get tokens
                tokens = super().post(request, *args, **kwargs)
                
                return Response({
                    'message': 'Login successful',
                    'tokens': tokens.data,
                    'user_type': 'farmer' if hasattr(user, 'farmer_profile') else 'buyer'
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'error': 'Invalid credentials'
                }, status=status.HTTP_401_UNAUTHORIZED)
                
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)