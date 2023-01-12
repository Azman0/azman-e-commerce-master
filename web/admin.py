from django.contrib import admin
from .models import Categories, Units, Products, Cart, SpecialProducts

# Register your models here.

class ProductsAdmin(admin.ModelAdmin):
    list_display = ('name', 'category_id', 'final_price', 'status', 'stock')
    search_fields = ['name', 'category_id__name', 'status', 'stock']

class SpecialProductsAdmin(admin.ModelAdmin):
    list_display = ('type', 'product_id')
    search_fields = ['type']

class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'status')
    search_fields = ['name', 'status']

admin.site.register(Products, ProductsAdmin)

admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Units)
admin.site.register(Cart)
admin.site.register(SpecialProducts, SpecialProductsAdmin)