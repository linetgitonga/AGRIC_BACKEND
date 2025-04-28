# crops/views.py
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
# import numpy as np
# from sklearn.neighbors import KNeighborsClassifier

from .models import Crop, SoilRecord, CropRecommendation
from .serializers import (
    CropSerializer, SoilRecordSerializer, 
    CropRecommendationSerializer, SoilInputSerializer
)

class CropViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Crop.objects.all()
    serializer_class = CropSerializer
    permission_classes = [permissions.IsAuthenticated]

class SoilRecordViewSet(viewsets.ModelViewSet):
    serializer_class = SoilRecordSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return SoilRecord.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# class CropRecommendationViewSet(viewsets.ReadOnlyModelViewSet):
#     serializer_class = CropRecommendationSerializer
#     permission_classes = [permissions.IsAuthenticated]
    
#     def get_queryset(self):
#         return CropRecommendation.objects.filter(user=self.request.user)
    
#     # @action(detail=False, methods=['post'])
#     # def recommend(self, request):
#     #     serializer = SoilInputSerializer(data=request.data)
#     #     if serializer.is_valid():
#     #         # Save soil record
#     #         soil_record = SoilRecord.objects.create(
#     #             user=request.user,
#     #             **serializer.validated_data
#     #         )
            
#     #         # Get crop recommendation using ML model
#     #         recommended_crop, confidence = self._get_crop_recommendation(
#     #             soil_record.nitrogen,
#     #             soil_record.phosphorus,
#     #             soil_record.potassium,
#     #             soil_record.ph_level,
#     #             soil_record.rainfall,
#     #             soil_record.temperature
#     #         )
            
#     #         # Create recommendation record
#     #         recommendation = CropRecommendation.objects.create(
#     #             user=request.user,
#     #             soil_record=soil_record,
#     #             recommended_crop=recommended_crop,
#     #             confidence_score=confidence,
#     #             recommendation_notes=f"Based on your soil parameters, {recommended_crop.name} is recommended with {confidence:.2f} confidence."
#     #         )
            
#     #         return Response(
#     #             CropRecommendationSerializer(recommendation).data,
#     #             status=status.HTTP_201_CREATED
#     #         )
#     #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     # def _get_crop_recommendation(self, n, p, k, ph, rainfall=None, temperature=None):
        """
        Simple crop recommendation logic.
        In a real system, this would use a trained ML model.
        """
        # This is a simplified example - in production, you'd use a proper trained model
        # For demo purposes, we'll just find the crop with the closest matching soil requirements
        
        crops = Crop.objects.all()
        if not crops:
            # Return a default or error if no crops in database
            return None, 0
            
        # Simple distance calculation to find best match
        min_distance = float('inf')
        best_crop = None
        
        for crop in crops:
            # Skip crops with missing data
            if None in (crop.min_nitrogen, crop.min_phosphorus, crop.min_potassium, crop.min_ph):
                continue
                
            # Calculate a simple distance metric
            n_dist = abs(n - (crop.min_nitrogen + crop.max_nitrogen) / 2 if crop.max_nitrogen else crop.min_nitrogen)
            p_dist = abs(p - (crop.min_phosphorus + crop.max_phosphorus) / 2 if crop.max_phosphorus else crop.min_phosphorus)
            k_dist = abs(k - (crop.min_potassium + crop.max_potassium) / 2 if crop.max_potassium else crop.min_potassium)
            ph_dist = abs(ph - (crop.min_ph + crop.max_ph) / 2 if crop.max_ph else crop.min_ph)
            
            # Add rainfall and temperature if available
            r_dist = t_dist = 0
            if rainfall is not None and crop.min_rainfall is not None:
                r_dist = abs(rainfall - (crop.min_rainfall + crop.max_rainfall) / 2 if crop.max_rainfall else crop.min_rainfall)
            
            if temperature is not None and crop.min_temperature is not None:
                t_dist = abs(temperature - (crop.min_temperature + crop.max_temperature) / 2 if crop.max_temperature else crop.min_temperature)
            
            # Total distance (weighted sum)
            distance = n_dist + p_dist + k_dist + (ph_dist * 2) + r_dist + t_dist
            
            if distance < min_distance:
                min_distance = distance
                best_crop = crop
        
        # Calculate a confidence score (inverted normalized distance)
        # Lower distance = higher confidence
        confidence = 1.0 / (1.0 + min_distance/10)  # Normalize to 0-1 range
        
        return best_crop, confidence