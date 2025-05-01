# crops/views.py
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
import logging
import os
import requests
from django.conf import settings
import pickle
import numpy as np

from .models import Crop, SoilRecord, CropRecommendation
from .serializers import (
    CropSerializer, SoilRecordSerializer, 
    CropRecommendationSerializer, SoilInputSerializer
)

class CropViewSet(viewsets.ModelViewSet):
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

# MODEL PROHGRAM
logger = logging.getLogger(__name__)

# Define paths for model files
MODEL_PATH = os.path.join(settings.BASE_DIR, 'MODEL', 'Crop_Recommender_model.pkl')
SCALER_PATH = os.path.join(settings.BASE_DIR, 'MODEL', 'scaler.pkl')
LABEL_ENCODER_PATH = os.path.join(settings.BASE_DIR, 'MODEL', 'label_encoder.pkl')

# Add these debug prints
print(f"BASE_DIR: {settings.BASE_DIR}")
print(f"Full MODEL_PATH: {MODEL_PATH}")
print(f"Model path exists: {os.path.exists(MODEL_PATH)}")
print(f"Scaler path exists: {os.path.exists(SCALER_PATH)}")
print(f"Label encoder path exists: {os.path.exists(LABEL_ENCODER_PATH)}")


def load_ml_components():
    try:
        # Check if files exist first
        if not os.path.exists(MODEL_PATH):
            logger.error(f"Model file not found at {MODEL_PATH}")
            return None, None, None
        if not os.path.exists(SCALER_PATH):
            logger.error(f"Scaler file not found at {SCALER_PATH}")
            return None, None, None
        if not os.path.exists(LABEL_ENCODER_PATH):
            logger.error(f"Label encoder file not found at {LABEL_ENCODER_PATH}")
            return None, None, None

        with open(MODEL_PATH, 'rb') as model_file:
            model = pickle.load(model_file)
        with open(SCALER_PATH, 'rb') as scaler_file:
            scaler = pickle.load(scaler_file)
        with open(LABEL_ENCODER_PATH, 'rb') as encoder_file:
            label_encoder = pickle.load(encoder_file)
        
        logger.info("Successfully loaded all ML components")
        return model, scaler, label_encoder
    except Exception as e:
        logger.error(f"Error loading ML components: {str(e)}")
        return None, None, None

model, scaler, label_encoder = load_ml_components()


class CropRecommendationViewSet(viewsets.ModelViewSet):
    serializer_class = CropRecommendationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return CropRecommendation.objects.filter(user=self.request.user)
    # TTTTTTTTTTTTTEEEEEEEEEEEEEEEEEEEEEEESSSSSSSSSSSSSSTTTTTTTTTTINGGGGGGGGGGG
    @action(detail=False, methods=['post'])
    def test_recommendation(self, request):

        
        """Test endpoint for crop recommendation"""
        test_data = {
            "nitrogen": 90,
            "phosphorus": 40,
            "potassium": 40,
            "ph_level": 6.5,
            "temperature": 25,
            "rainfall": 2000,
            "latitude": 1.2921,  
            "longitude": 36.8219
        }
        
        try:
            # Test model components
            if model is None or scaler is None or label_encoder is None:
                return Response(
                    {"error": "ML components not loaded",
                    "model": model is not None,
                    "scaler": scaler is not None,
                    "label_encoder": label_encoder is not None},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            # Test crop recommendation
            recommended_crop, confidence = self._get_crop_recommendation(
                test_data["nitrogen"],
                test_data["phosphorus"],
                test_data["potassium"],
                test_data["ph_level"],
                test_data["rainfall"],
                test_data["temperature"]
            )
            
            if recommended_crop:
                return Response({
                    "status": "success",
                    "crop": recommended_crop.name,
                    "confidence": confidence,
                    "input_data": test_data
                })
            else:
                return Response(
                    {"error": "No crop recommendation found"},
                    status=status.HTTP_404_NOT_FOUND
                )
                
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



#EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEENNNNNNNNNNNNNNNNNNNNDDDDDDDDDDDDDDDDD 

    @action(detail=False, methods=['post'])
    def recommend(self, request):
        try:
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
                logger.debug(f"Weather data received: {weather_data}")
            except Exception as e:
                logger.error(f"Weather data fetch error: {str(e)}")
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
                'humidity': weather_data.get('humidity', 0),
                **request.data  # Include other soil parameters from request
            }
            logger.debug(f"Combined data for serializer: {data}")
            
            serializer = SoilInputSerializer(data=data)
            if serializer.is_valid():
                try:
                    # Save soil record
                    soil_record = SoilRecord.objects.create(
                        user=request.user,
                        # temperature=weather_data['temperature'],
                        # rainfall=weather_data['rainfall'],
                        # humidity=weather_data.get('humidity', 0),  # Explicitly set humidity
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
        except Exception as e:
            logger.error(f"Unexpected error in recommend view: {str(e)}", exc_info=True)
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def _get_weather_data(self, latitude, longitude):
        """
        Fetch weather data from Tomorrow.io API
        """
        try:
            api_key = settings.TOMORROW_IO_API_KEY  # Add this to your settings.py
            url = f"https://api.tomorrow.io/v4/weather/forecast"
            
            params = {
                'location': f"{latitude},{longitude}",
                'apikey': api_key,
                'fields': ['temperature', 'precipitationIntensity', 'humidity'],
                # 'timesteps': 'daily'
            }
            logger.debug(f"Requesting weather data for coordinates: {latitude}, {longitude}")
            
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raises an HTTPError for bad responses
                
            data = response.json()
            logger.debug(f"Weather API response: {data}")
            # Extract current temperature and precipitation from the response
            current_data = data['timelines']['minutely'][0]['values']
            daily_data = data['timelines']['daily'][0]['values']

            # Convert precipitation intensity to daily rainfall in mm
            # precipitationIntensity is in mm/hr, multiply by 24 for daily estimate
            daily_rainfall = daily_data.get('precipitationIntensity', 0) * 24
            

            return {
                'temperature': current_data['temperature'],
                'rainfall': daily_rainfall, # mm/hr
                'humidity': current_data.get('humidity', 0)  # relative humidity %  # mm/hr
            }
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch weather data: {str(e)}")
            raise Exception("Failed to fetch weather data")
        except KeyError as e:
            logger.error(f"Invalid response format: {str(e)}")
            raise Exception("Invalid weather data format")


            
    
    def _get_crop_recommendation(self, n, p, k, ph, rainfall=None, temperature=None, humidity=None):
        """
        Get crop recommendation using the loaded pickle model
        """
        try:
            if model is None or scaler is None or label_encoder is None:
                raise Exception("ML components not properly loaded")

            # Log input values
            logger.debug(f"Input values: N={n}, P={p}, K={k}, pH={ph}, Rain={rainfall}, Temp={temperature} , Humidity={humidity}")

            # Prepare input data for model
            input_data = np.array([[n, p, k, temperature, rainfall, ph]])
            logger.debug(f"Input array shape: {input_data.shape}")
            
            # Scale the input data
            try:
                scaled_features = scaler.transform(input_data)
                logger.debug(f"Scaled features: {scaled_features}")
            except Exception as scale_error:
                logger.error(f"Error scaling features: {str(scale_error)}")
                raise Exception(f"Error scaling features: {str(scale_error)}")

            # Make prediction
            try:
                prediction = model.predict(scaled_features)
                prediction_proba = model.predict_proba(scaled_features)
                logger.debug(f"Raw prediction: {prediction}, probabilities: {prediction_proba}")
            except Exception as pred_error:
                logger.error(f"Error making prediction: {str(pred_error)}")
                raise Exception(f"Error making prediction: {str(pred_error)}")
            
            
            # Log prediction details
            predicted_crop_name = label_encoder.inverse_transform(prediction)[0]
            confidence = np.max(prediction_proba[0])
            logger.debug(f"Predicted crop: {predicted_crop_name}, Confidence: {confidence}")
            
            # Get all possible crop names from label encoder
            possible_crops = label_encoder.classes_
            logger.debug(f"Possible crops from model: {possible_crops}")
            
            # Get all crop names from database
            db_crops = list(Crop.objects.values_list('name', flat=True))
            logger.debug(f"Crops in database: {db_crops}")
            
            # Get the corresponding crop from database
            try:
                recommended_crop = Crop.objects.get(name__iexact=predicted_crop_name)
                logger.info(f"Found matching crop in database: {recommended_crop.name}")
                return recommended_crop, confidence
            except Crop.DoesNotExist:
                logger.error(f"Predicted crop '{predicted_crop_name}' not found in database")
                return None, 0
                
        except Exception as e:
            logger.error(f"Error in crop recommendation: {str(e)}", exc_info=True)
            return None, 0