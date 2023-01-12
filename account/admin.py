from django.contrib import admin
from .models import Clients, Orders

# Register your models here.

class OrdersAdmin(admin.ModelAdmin):
    list_display = ('id', 'mobile', 'full_name', 'total_cost', 'status', 'created_at', 'address')
    readonly_fields = ['mobile', 'cart_no', 'client', 'full_name', 'address', 'cost', 'delivery_fees', 'total_cost', 'created_at']
    search_fields = ['mobile', 'full_name', 'status']

admin.site.register(Orders, OrdersAdmin)