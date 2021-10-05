import django_filters
from django_filters import DateFilter
from django import forms

from .models import *


class PartFilter(django_filters.FilterSet):
    class Meta:
        model = Part
        fields = ['partno', 'product', 'supplier']


class DIFilter(django_filters.FilterSet):
    created_date = django_filters.CharFilter( widget=forms.TextInput(attrs={
            'placeholder': 'YYYY-MM-DD'}))
    class Meta:
        model = DeliveryIns
        fields = ['product', 'supplier', 'created_date']
        
        

class DOFilter(django_filters.FilterSet):
    class Meta:
        model = DeliveryOrder
        fields = ['supplier']


class POFilter(django_filters.FilterSet):
    created_date = django_filters.CharFilter( widget=forms.TextInput(attrs={
            'placeholder': 'YYYY-MM-DD'}))
    class Meta:
        model = Order
        fields = ['product', 'supplier', 'created_date']
