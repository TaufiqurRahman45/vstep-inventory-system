from django.contrib import admin

from .models import (
    Supplier,
    Purchaseorder,
    Season,
    Drop,
    Product,
    Order,
    Delivery
)

class SupplierAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'address', 'created_date']

class PurchaseorderAdmin(admin.ModelAdmin):
    list_display = [ 'name', 'partno']

admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Purchaseorder, PurchaseorderAdmin)
admin.site.register(Season)
admin.site.register(Drop)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Delivery)