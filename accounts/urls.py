# accounts/urls.py
from django.urls import path
from .views import RegisterView, UserProfileView, FarmerProfileView, BuyerProfileView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('farmer-profile/', FarmerProfileView.as_view(), name='farmer-profile'),
    path('buyer-profile/', BuyerProfileView.as_view(), name='buyer-profile'),
]
