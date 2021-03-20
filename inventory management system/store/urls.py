from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

from .views import (
    create_supplier,
    create_product,
    create_order,

    SupplierListView,
    ProductListView,
    OrderListView,
    update_Order,
)

urlpatterns = [
    path('create-supplier/', create_supplier, name='create-supplier'),
    path('create-product/', create_product, name='create-product'),
    path('create-order/', create_order, name='create-order'),

    path('supplier-list/', SupplierListView.as_view(), name='supplier-list'),
    path('product-list/', ProductListView.as_view(), name='product-list'),
    path('order-list/', OrderListView.as_view(), name='order-list'),
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),

]