from django.contrib import admin

from .models import (
    Supplier,
    Product,
    Order,
    Part,
    PurchaseOrder,
)

class SupplierAdmin(admin.ModelAdmin):
    list_display = [ 'name', 'address', 'email', 'created_date']

admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Part)
admin.site.register(PurchaseOrder)
