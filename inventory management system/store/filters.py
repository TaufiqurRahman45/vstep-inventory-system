import django_filters
from django_filters import DateFilter

from .models import *

class PartFilter(django_filters.FilterSet):

    class Meta:
        model = Part
        fields = ['partno', 'product', 'supplier']
        

class DIFilter(django_filters.FilterSet):

    class Meta:
        model = DeliveryIns
        fields = ['supplier']

class DOFilter(django_filters.FilterSet):

    class Meta:
        model = DeliveryOrder
        fields = ['supplier']

class POFilter(django_filters.FilterSet):

    class Meta:
        model = Order
        fields = ['product','supplier']