from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

from .views import (
    create_supplier,
    create_product,
    create_order,
    create_part,
    create_deliveryorder,
    create_deliveryins,

    SupplierListView,
    ProductListView,
    OrderListView,
    PartListView,
    DeliveryOrderListView,
    logs,
    generate_pdf,
    generate_pdf_part,
    # generate_pdf_po,
    generate_pdf_do,
    generate_pdf_di,
    DeliveryInsListView,
)

urlpatterns = [
    path('create-supplier/', create_supplier, name='create-supplier'),

    path('create-product/', create_product, name='create-product'),

    path('create-order/', create_order.as_view(), name='create-order'),

    path('create-part/', create_part, name='create-part'),

    path('create-deliveryorder/', create_deliveryorder, name='create-deliveryorder'),

    path('create-deliveryins/', create_deliveryins, name='create-deliveryins'),

    path('logs/', logs, name='logs'),


    path('supplier-list/', SupplierListView.as_view(), name='supplier-list'),

    path('product-list/', ProductListView.as_view(), name='product-list'),

    path('order-list/', OrderListView.as_view(), name='order-list'),

    path('part-list/', PartListView.as_view(), name='part-list'),

    path('do-list/', DeliveryOrderListView.as_view(), name='do-list'),

    path('dins-list/', DeliveryInsListView.as_view(), name='dins-list'),

    path('generate-pdf/', generate_pdf, name='generate-pdf'),

    path('generate-pdf_part/', generate_pdf_part, name='generate-pdf_part'),

    path('generate-pdf_do/', generate_pdf_do, name='generate-pdf_do'),

    path('generate-pdf_di/', generate_pdf_di, name='generate-pdf_di'),

    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),

    path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),

    path('update_part/<str:pk>/', views.updatePart, name="update_part"),

    path('delete_part/<str:pk>/', views.deletePart, name="delete_part"),

    path('update_do/<str:pk>/', views.updateDO, name="update_do"),

    path('delete_do/<str:pk>/', views.deleteDO, name="delete_do"),

    path('update_di/<str:pk>/', views.updateDI, name="update_di"),

    path('delete_di/<str:pk>/', views.deleteDI, name="delete_di"),
]