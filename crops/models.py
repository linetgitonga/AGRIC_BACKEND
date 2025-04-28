# crops/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Crop(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='crops/', blank=True, null=True)
    growing_season = models.CharField(max_length=100, blank=True, null=True)
    average_yield = models.FloatField(help_text="Average yield per acre", blank=True, null=True)
    growing_time = models.IntegerField(help_text="Days to harvest", blank=True, null=True)
    
    # Optimal growing conditions
    min_temperature = models.FloatField(help_text="Minimum temperature in °C", blank=True, null=True)
    max_temperature = models.FloatField(help_text="Maximum temperature in °C", blank=True, null=True)
    min_rainfall = models.FloatField(help_text="Minimum rainfall in mm", blank=True, null=True)
    max_rainfall = models.FloatField(help_text="Maximum rainfall in mm", blank=True, null=True)
    
    # Optimal soil conditions
    min_nitrogen = models.FloatField(help_text="Minimum nitrogen (N) requirement", blank=True, null=True)
    max_nitrogen = models.FloatField(help_text="Maximum nitrogen (N) tolerance", blank=True, null=True)
    min_phosphorus = models.FloatField(help_text="Minimum phosphorus (P) requirement", blank=True, null=True)
    max_phosphorus = models.FloatField(help_text="Maximum phosphorus (P) tolerance", blank=True, null=True)
    min_potassium = models.FloatField(help_text="Minimum potassium (K) requirement", blank=True, null=True)
    max_potassium = models.FloatField(help_text="Maximum potassium (K) tolerance", blank=True, null=True)
    min_ph = models.FloatField(help_text="Minimum pH level", blank=True, null=True)
    max_ph = models.FloatField(help_text="Maximum pH level", blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class SoilRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location_name = models.CharField(max_length=100)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    
    # Soil parameters
    nitrogen = models.FloatField(help_text="Nitrogen (N) content")
    phosphorus = models.FloatField(help_text="Phosphorus (P) content")
    potassium = models.FloatField(help_text="Potassium (K) content")
    ph_level = models.FloatField(help_text="pH level")
    
    # Climate parameters
    rainfall = models.FloatField(help_text="Average rainfall in mm", blank=True, null=True)
    temperature = models.FloatField(help_text="Average temperature in °C", blank=True, null=True)
    humidity = models.FloatField(help_text="Average humidity percentage", blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.location_name} - {self.user.email}"

class CropRecommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    soil_record = models.ForeignKey(SoilRecord, on_delete=models.CASCADE)
    recommended_crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    confidence_score = models.FloatField(help_text="Confidence score from 0 to 1")
    recommendation_notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.soil_record.location_name} - {self.recommended_crop.name}"