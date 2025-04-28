from django.contrib import admin
from .models import Product, ProductImage, Order, OrderItem, Review

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'seller', 'crop', 'price_per_unit', 'quantity_available', 'status', 'created_at')
    list_filter = ('status', 'is_organic', 'is_featured', 'created_at')
    search_fields = ('title', 'description', 'seller__email')
    inlines = [ProductImageInline]

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'buyer', 'status', 'payment_status', 'total_amount', 'created_at')
    list_filter = ('status', 'payment_status', 'created_at')
    search_fields = ('order_number', 'buyer__email', 'shipping_address')
    inlines = [OrderItemInline]

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('product__title', 'user__email', 'comment')

admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Review, ReviewAdmin)