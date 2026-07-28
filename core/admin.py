from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Brand, Product

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'is_active')
    search_fields = ('name', 'code')
    list_filter = ('is_active',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('item_code', 'brand', 'family', 'subfamily', 'origin', 'is_truck_mounted')
    search_fields = ('item_code', 'description', 'family')
    list_filter = ('brand', 'origin', 'is_truck_mounted')
