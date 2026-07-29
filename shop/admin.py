from django.contrib import admin
from .models import Category, Product, PromoCode, Color

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon']
    prepopulated_fields = {'slug': ('name',)}
    fields = ['name', 'slug', 'icon', 'image']

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'in_stock', 'created_at']
    list_filter = ['category', 'in_stock', 'colors']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ['colors']

@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount', 'is_active', 'valid_until']
    list_filter = ['is_active']
    search_fields = ['code']