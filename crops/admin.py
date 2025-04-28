from django.contrib import admin
from .models import Crop, SoilRecord, CropRecommendation

class CropAdmin(admin.ModelAdmin):
    list_display = ('name', 'growing_season', 'growing_time', 'min_temperature', 'max_temperature')
    search_fields = ('name', 'description')
    list_filter = ('growing_season',)

class SoilRecordAdmin(admin.ModelAdmin):
    list_display = ('location_name', 'user', 'nitrogen', 'phosphorus', 'potassium', 'ph_level', 'created_at')
    search_fields = ('location_name', 'user__email')
    list_filter = ('created_at',)

class CropRecommendationAdmin(admin.ModelAdmin):
    list_display = ('user', 'soil_record', 'recommended_crop', 'confidence_score', 'created_at')
    search_fields = ('user__email', 'soil_record__location_name')
    list_filter = ('created_at', 'confidence_score')

admin.site.register(Crop, CropAdmin)
admin.site.register(SoilRecord, SoilRecordAdmin)
admin.site.register(CropRecommendation, CropRecommendationAdmin)