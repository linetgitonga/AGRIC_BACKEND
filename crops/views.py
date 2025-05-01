# crops/views.py
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
import logging
import os
import requests
from django.conf import settings
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
        
        
        # """
        # Simple crop recommendation logic.
        # In a real system, this would use a trained ML model.
        # """
        # # This is a simplified example - in production, you'd use a proper trained model
        # # For demo purposes, we'll just find the crop with the closest matching soil requirements
        
        # crops = Crop.objects.all()
        # if not crops:
        #     # Return a default or error if no crops in database
        #     return None, 0
            
        # # Simple distance calculation to find best match
        # min_distance = float('inf')
        # best_crop = None
        
        # for crop in crops:
        #     # Skip crops with missing data
        #     if None in (crop.min_nitrogen, crop.min_phosphorus, crop.min_potassium, crop.min_ph):
        #         continue
                
        #     # Calculate a simple distance metric
        #     n_dist = abs(n - (crop.min_nitrogen + crop.max_nitrogen) / 2 if crop.max_nitrogen else crop.min_nitrogen)
        #     p_dist = abs(p - (crop.min_phosphorus + crop.max_phosphorus) / 2 if crop.max_phosphorus else crop.min_phosphorus)
        #     k_dist = abs(k - (crop.min_potassium + crop.max_potassium) / 2 if crop.max_potassium else crop.min_potassium)
        #     ph_dist = abs(ph - (crop.min_ph + crop.max_ph) / 2 if crop.max_ph else crop.min_ph)
            
        #     # Add rainfall and temperature if available
        #     r_dist = t_dist = 0
        #     if rainfall is not None and crop.min_rainfall is not None:
        #         r_dist = abs(rainfall - (crop.min_rainfall + crop.max_rainfall) / 2 if crop.max_rainfall else crop.min_rainfall)
            
        #     if temperature is not None and crop.min_temperature is not None:
        #         t_dist = abs(temperature - (crop.min_temperature + crop.max_temperature) / 2 if crop.max_temperature else crop.min_temperature)
            
        #     # Total distance (weighted sum)
        #     distance = n_dist + p_dist + k_dist + (ph_dist * 2) + r_dist + t_dist
            
        #     if distance < min_distance:
        #         min_distance = distance
        #         best_crop = crop
        
        # # Calculate a confidence score (inverted normalized distance)
        # # Lower distance = higher confidence
        # confidence = 1.0 / (1.0 + min_distance/10)  # Normalize to 0-1 range
        
        # return best_crop, confidence




# MODEL PROHGRAM

logger = logging.getLogger(__name__)

# Load the ML model
MODEL_PATH = os.path.join(settings.BASE_DIR, 'ml_models', 'agric.h5')

def load_ml_model():
    try:
        return tf.keras.models.load_model(MODEL_PATH)
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        return None

model = load_ml_model()




class CropRecommendationViewSet(viewsets.ModelViewSet):
    serializer_class = CropRecommendationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return CropRecommendation.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def recommend(self, request):
        # Get location data from request
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')
        
        if not latitude or not longitude:
            return Response(
                {"error": "Location data is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Fetch weather data from OpenWeatherMap API
        try:
            weather_data = self._get_weather_data(latitude, longitude)
        except Exception as e:
            return Response(
                {"error": f"Failed to fetch weather data: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Combine weather data with soil parameters
        data = {
            'latitude': latitude,
            'longitude': longitude,
            'temperature': weather_data['temperature'],
            'rainfall': weather_data['rainfall'],
            **request.data  # Include other soil parameters from request
        }
        
        serializer = SoilInputSerializer(data=data)
        if serializer.is_valid():
            try:
                # Save soil record
                soil_record = SoilRecord.objects.create(
                    user=request.user,
                    **serializer.validated_data
                )
                
                # Get crop recommendation using ML model
                recommended_crop, confidence = self._get_crop_recommendation(
                    soil_record.nitrogen,
                    soil_record.phosphorus,
                    soil_record.potassium,
                    soil_record.ph_level,
                    soil_record.rainfall,
                    soil_record.temperature
                )
            
                if not recommended_crop:
                    return Response(
                        {"error": "No suitable crop found"},
                        status=status.HTTP_404_NOT_FOUND
                    )
            
                # Create recommendation record
                recommendation = CropRecommendation.objects.create(
                    user=request.user,
                    soil_record=soil_record,
                    recommended_crop=recommended_crop,
                    confidence_score=confidence,
                    recommendation_notes=f"Based on your soil parameters and local weather conditions, {recommended_crop.name} is recommended with {confidence:.2f} confidence."
                )
            
                return Response(
                    CropRecommendationSerializer(recommendation).data,
                    status=status.HTTP_201_CREATED
                )
            
            except Exception as e:
                logger.error(f"Error in recommendation process: {str(e)}")
                return Response(
                    {"error": "Failed to process recommendation"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
                
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def _get_weather_data(self, latitude, longitude):
        """
        Fetch weather data from OpenWeatherMap API
        """
        api_key = settings.OPENWEATHERMAP_API_KEY  # Add this to your settings.py
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&units=metric"
        
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception("Failed to fetch weather data")
            
        data = response.json()
        
        return {
            'temperature': data['main']['temp'],
            'rainfall': data.get('rain', {}).get('1h', 0)  # Rainfall in last hour, default to 0
        }

    def _get_crop_recommendation(self, n, p, k, ph, rainfall=None, temperature=None):
        """
        Get crop recommendation using the loaded ML model
        """
        try:
            if model is None:
                raise Exception("ML model not loaded")

            # Prepare input data for model
            input_data = np.array([[n, p, k, ph, rainfall, temperature]])
            
            # Make prediction
            prediction = model.predict(input_data)
            
            # Get the predicted crop index
            crop_index = np.argmax(prediction[0])
            confidence = float(prediction[0][crop_index])
            
            # Get the corresponding crop from database
            try:
                recommended_crop = Crop.objects.all()[crop_index]
            except IndexError:
                return None, 0
                
            logger.info(f"Prediction successful: Crop={recommended_crop.name}, Confidence={confidence}")
            return recommended_crop, confidence
            
        except Exception as e:
            logger.error(f"Error in crop recommendation: {str(e)}")
            return None, 0
         