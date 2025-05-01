# crops/serializers.py
from rest_framework import serializers
from .models import Crop, SoilRecord, CropRecommendation

class CropSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crop
        fields = '__all__'

class SoilRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoilRecord
        fields = '__all__'
        read_only_fields = ('user',)

class CropRecommendationSerializer(serializers.ModelSerializer):
    recommended_crop = CropSerializer(read_only=True)
    soil_record = SoilRecordSerializer(read_only=True)
    
    class Meta:
        model = CropRecommendation
        fields = '__all__'
        read_only_fields = ('user', 'confidence_score', 'recommendation_notes')

class SoilInputSerializer(serializers.Serializer):
    location_name = serializers.CharField(max_length=100 ,required=False)
    latitude = serializers.FloatField(required=False)
    longitude = serializers.FloatField(required=False)
    nitrogen = serializers.FloatField()
    phosphorus = serializers.FloatField()
    potassium = serializers.FloatField()
    ph_level = serializers.FloatField()
    rainfall = serializers.FloatField(required=False)
    temperature = serializers.FloatField(required=False)
    humidity = serializers.FloatField(required=False)