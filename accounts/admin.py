# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, FarmerProfile, BuyerProfile

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'user_type', 'is_active', 'date_joined')
    list_filter = ('user_type', 'is_active', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'user_type')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'user_type', 'first_name', 'last_name'),
        }),
    )

class FarmerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'farm_size', 'experience_years')
    search_fields = ('user__email', 'phone_number')
    list_filter = ('experience_years',)

class BuyerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'business_type', 'phone_number')
    search_fields = ('user__email', 'company_name', 'phone_number')
    list_filter = ('business_type',)

admin.site.register(User, CustomUserAdmin)
admin.site.register(FarmerProfile, FarmerProfileAdmin)
admin.site.register(BuyerProfile, BuyerProfileAdmin)