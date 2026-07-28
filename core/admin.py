from django.contrib import admin
from .models import Brand, Product, PurchaseRequest

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


@admin.register(PurchaseRequest)
class PurchaseRequestAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'unit_cost_usd', 'requested_by', 'created_at')
    search_fields = ('product__item_code', 'requested_by')
    list_filter = ('product__brand', 'created_at')
