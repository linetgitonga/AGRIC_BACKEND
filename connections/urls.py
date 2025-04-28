from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ContractRequestViewSet, 
    BuyerPreferenceViewSet, 
    FarmerOfferViewSet, 
    ConnectionViewSet, 
    MessageViewSet
)

router = DefaultRouter()
router.register(r'contract-requests', ContractRequestViewSet, basename='contract-request')
router.register(r'buyer-preferences', BuyerPreferenceViewSet, basename='buyer-preference')
router.register(r'farmer-offers', FarmerOfferViewSet, basename='farmer-offer')
router.register(r'connections', ConnectionViewSet, basename='connection')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
]