from django.contrib import admin

from .models import (
    Supplier,
    Season,
    Drop,
    Product,
    Order,
    Delivery
)

class SupplierAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'address', 'created_date']



admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Season)
admin.site.register(Drop)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Delivery)