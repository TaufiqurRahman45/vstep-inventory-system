from django import forms

from .models import Product, Order


class SupplierForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'name',
        'data-val': 'true',
        'data-val-required': 'Please enter name',
    }))
    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'address',
        'data-val': 'true',
        'data-val-required': 'Please enter address',
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'id': 'email',
        'data-val': 'true',
        'data-val-required': 'Please enter email',
    }))

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'sortno']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'name'}),
            'sortno': forms.NumberInput(attrs={'class': 'form-control', 'id': 'sortno'})
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['supplier', 'product', 'partno', 'description', 'style', 'standard', 'quantity', 'limit', 'is_ppc', 'new_stock']

        widgets = {
            'supplier': forms.Select(attrs={'class': 'form-control', 'id': 'supplier'}),
            'product': forms.Select(attrs={'class': 'form-control', 'id': 'product'}),
            'partno': forms.TextInput(attrs={'class': 'form-control', 'id': 'partno'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'id': 'description'}),
            'style': forms.TextInput(attrs={'class': 'form-control', 'id': 'description'}),
            'standard': forms.NumberInput(attrs={'class': 'form-control', 'id': 'standard'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'id': 'quantity'}),
            'limit' : forms.NumberInput(attrs={'class': 'form-control', 'id': 'limit'}),
            'is_ppc' : forms.Select(attrs={'class': 'form-control', 'id': 'is_ppc'}),
            'new_stock' : forms. NumberInput(attrs={'class': 'form-control', 'id': 'new_stock'}),
        }

