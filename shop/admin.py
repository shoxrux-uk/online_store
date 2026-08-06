from django.contrib import admin
from .models import Category, Product, PromoCode, Color, ProductImage, Size, Order, OrderItem

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3
    fields = ['image', 'is_main']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon']
    prepopulated_fields = {'slug': ('name',)}
    fields = ['name', 'slug', 'icon', 'image']

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['name', 'category_type', 'sort_order']
    list_filter = ['category_type']
    search_fields = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'in_stock', 'created_at']
    list_filter = ['category', 'in_stock', 'colors', 'sizes']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ['colors', 'sizes']
    inlines = [ProductImageInline]

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image', 'is_main']
    list_filter = ['product']

@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount', 'is_active', 'valid_until']
    list_filter = ['is_active']
    search_fields = ['code']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'full_name', 'phone', 'total_price', 'payment_method', 'status', 'created_at']
    list_filter = ['status', 'payment_method']
    search_fields = ['full_name', 'phone', 'email', 'user__username']
    readonly_fields = ['created_at']
    list_editable = ['status']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price']
    list_filter = ['order']