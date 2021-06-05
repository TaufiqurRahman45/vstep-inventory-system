from django import forms

from .models import Product, Order, Part, DeliveryOrder,DeliveryIns


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
    address2 = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'address2',
        'data-val': 'true',
        'data-val-required': 'Please enter address',
    }))
    address3 = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'address3',
        'data-val': 'true',
        'data-val-required': 'Please enter address',
    }))
    postcode = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'postcode',
        'data-val': 'true',
        'data-val-required': 'Please enter address',
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'id': 'email',
        'data-val': 'true',
        'data-val-required': 'Please enter email',
    }))
    phone = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'phone',
        'data-val': 'true',
        'data-val-required': 'Please enter phone number',
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
        fields = ['supplier', 'product', 'part', 'style', 'standard', 'quantity', 'limit', 'is_ppc', 'tax', 'price', 'unit', 'terms', 'remarks', 'new_stock']

        widgets = {
            'supplier': forms.Select(attrs={'class': 'form-control', 'id': 'supplier'}),
            'product': forms.Select(attrs={'class': 'form-control', 'id': 'product'}),
            'part': forms.Select(attrs={'class': 'form-control', 'id': 'part'}),
            'style': forms.TextInput(attrs={'class': 'form-control', 'id': 'description'}),
            'standard': forms.NumberInput(attrs={'class': 'form-control', 'id': 'standard'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'id': 'quantity'}),
            'limit' : forms.NumberInput(attrs={'class': 'form-control', 'id': 'limit'}),
            'is_ppc' : forms.Select(attrs={'class': 'form-control', 'id': 'is_ppc'}),
            'tax' : forms. NumberInput(attrs={'class': 'form-control', 'id': 'tax'}),
            'price' : forms. NumberInput(attrs={'class': 'form-control', 'id': 'price'}),
            'unit' : forms. NumberInput(attrs={'class': 'form-control', 'id': 'unit'}),
            'terms': forms.Select(attrs={'class': 'form-control', 'id': 'terms'}),
            'remarks': forms.Select(attrs={'class': 'form-control', 'id': 'remarks'}),
            'new_stock' : forms. NumberInput(attrs={'class': 'form-control', 'id': 'new_stock'}),
        }

class PartForm(forms.ModelForm):
    class Meta:
        model = Part
        fields = ['partno', 'partname', 'stylepack', 'standardpack', 'supplier', 'product', 'unit', 'price', 'tax', ]

        widgets = {
            'partno': forms.TextInput(attrs={'class': 'form-control', 'id': 'partno'}),
            'partname': forms.TextInput(attrs={'class': 'form-control', 'id': 'partname'}),
            'stylepack': forms.TextInput(attrs={'class': 'form-control', 'id': 'stylepack'}),
            'standardpack': forms.NumberInput(attrs={'class': 'form-control', 'id': 'standardpack'}),
            'supplier': forms.Select(attrs={'class': 'form-control', 'id': 'supplier'}),
            'product': forms.Select(attrs={'class': 'form-control', 'id': 'product'}),
            'unit': forms.NumberInput(attrs={'class': 'form-control', 'id': 'unit'}),
            'price' : forms.NumberInput(attrs={'class': 'form-control', 'id': 'price'}),
        }

class DeliveryOrderForm(forms.ModelForm):
    class Meta:
        model = DeliveryOrder
        fields = ['supplier','do_quantity', 'order']

        widgets = {
            'supplier' : forms.Select(attrs={'class': 'form-control', 'id': 'supplier'}),
            'do_quantity': forms.NumberInput(attrs={'class': 'form-control', 'id': 'do_quantity'}),
            'order': forms.Select(attrs={'class': 'form-control', 'id': 'order'})
        }


class DeliveryInsForm(forms.ModelForm):
    class Meta:
        model = DeliveryIns
        fields = ['variant','usage',  'supplier', 'dimension', 'box', 'remarks','order']

        widgets = {
            'order': forms.Select(attrs={'class': 'form-control', 'id': 'order'}),
            'variant': forms.Select(attrs={'class': 'form-control', 'id': 'variant'}),
            'usage' : forms.NumberInput(attrs={'class': 'form-control', 'id': 'usage'}),
            'supplier': forms.Select(attrs={'class': 'form-control', 'id': 'supplier'}),
            'dimension': forms.TextInput(attrs={'class': 'form-control', 'id': 'dimension'}),
            'box': forms.NumberInput(attrs={'class': 'form-control', 'id': 'box'}),
            'remarks': forms.TextInput(attrs={'class': 'form-control', 'id': 'remarks'}),
        }