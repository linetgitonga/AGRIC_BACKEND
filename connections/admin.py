from django.contrib import admin
from .models import ContractRequest, BuyerPreference, FarmerOffer, Connection, Message

class ContractRequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'buyer', 'farmer', 'crop', 'status', 'delivery_date', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'buyer__email', 'farmer__email')

class BuyerPreferenceAdmin(admin.ModelAdmin):
    list_display = ('buyer', 'is_organic_preferred')
    search_fields = ('buyer__email', 'preferred_regions')
    filter_horizontal = ('preferred_crops',)

class FarmerOfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'farmer', 'crop', 'quantity_available', 'price_per_unit', 'status')
    list_filter = ('status', 'is_organic', 'created_at')
    search_fields = ('title', 'farmer__email', 'description')

class ConnectionAdmin(admin.ModelAdmin):
    list_display = ('initiator', 'receiver', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('initiator__email', 'receiver__email')

class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'subject', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('sender__email', 'receiver__email', 'subject', 'content')

admin.site.register(ContractRequest, ContractRequestAdmin)
admin.site.register(BuyerPreference, BuyerPreferenceAdmin)
admin.site.register(FarmerOffer, FarmerOfferAdmin)
admin.site.register(Connection, ConnectionAdmin)
admin.site.register(Message, MessageAdmin)