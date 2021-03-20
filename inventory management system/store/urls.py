from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

from .views import (
    create_supplier,
    create_season,
    create_drop,
    create_product,
    create_order,
    create_delivery,

    SupplierListView,
    SeasonListView,
    DropListView,
    ProductListView,
    OrderListView,
    DeliveryListView,
    update_Order,
)

urlpatterns = [
    path('create-supplier/', create_supplier, name='create-supplier'),
    path('create-season/', create_season, name='create-season'),
    path('create-drop/', create_drop, name='create-drop'),
    path('create-product/', create_product, name='create-product'),
    path('create-order/', create_order, name='create-order'),
    path('create-delivery/', create_delivery, name='create-delivery'),

    path('supplier-list/', SupplierListView.as_view(), name='supplier-list'),
    path('season-list/', SeasonListView.as_view(), name='season-list'),
    path('drop-list/', DropListView.as_view(), name='drop-list'),
    path('product-list/', ProductListView.as_view(), name='product-list'),
    path('order-list/', OrderListView.as_view(), name='order-list'),
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    path('delivery-list/', DeliveryListView.as_view(), name='delivery-list'),
    path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),

]