from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CropViewSet, 
    SoilRecordViewSet
    # CropRecommendationViewSet
)

router = DefaultRouter()

# Register viewsets with the router
router.register(r'crops', CropViewSet, basename='crop')
router.register(r'soil-records', SoilRecordViewSet, basename='soil-record')
# router.register(r'recommendations', CropRecommendationViewSet, basename='recommendation')

urlpatterns = [
    path('', include(router.urls)),
    # Custom endpoint for crop recommendations
    # path('recommendations/recommend/', 
    #      CropRecommendationViewSet.as_view({'post': 'recommend'}), 
    #      name='crop-recommendation'),
]