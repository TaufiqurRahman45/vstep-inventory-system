from django import forms
from django.forms import modelformset_factory
from django.forms.widgets import NumberInput

from django.forms.widgets import NumberInput

from .models import Product, Order, Part,DeliveryIns, DeliveryOrder


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
    attn = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'attn',
        'data-val': 'true',
        'data-val-required': 'Please enter Attn name',
    }))
    attn_email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'id': 'attn_email',
        'data-val': 'true',
        'data-val-required': 'Please enter Attn email',
    }))

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'name'}),
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['supplier', 'product', 'part', 'quantity',  'is_ppc', 'terms', 'remarks', 'new_stock', 'po_id', 'created_date']
        created_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
        widgets = {
            'po_id': forms.NumberInput(attrs={'class': 'form-control', 'id': 'po_id', 'readonly':'readonly'}),
            'supplier': forms.Select(attrs={'class': 'form-control', 'id': 'supplier'}),
            'product': forms.Select(attrs={'class': 'form-control', 'id': 'product'}),
            'part': forms.Select(attrs={'class': 'form-control', 'id': 'part'}),        
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'id': 'quantity'}),
            'is_ppc' : forms.Select(attrs={'class': 'form-control', 'id': 'is_ppc'}),
            'terms': forms.Select(attrs={'class': 'form-control', 'id': 'terms'}),
            'remarks': forms.Select(attrs={'class': 'form-control', 'id': 'remarks'}),
            'new_stock' : forms.NumberInput(attrs={'class': 'form-control', 'id': 'new_stock'}),
        }


    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['part'].queryset = Part.objects.none()

            if 'supplier' in self.data:
                try:
                    supplier_id = int(self.data.get('supplier'))
                    self.fields['part'].queryset = Part.objects.filter(supplier_id=supplier_id).order_by('partname')
                except (ValueError, TypeError):
                    pass 
            elif self.instance.pk:
                self.fields['part'].queryset = self.instance.supplier.part_set.order_by('partname')
                
class PartForm(forms.ModelForm):
    class Meta:
        model = Part
        fields = ['partno', 'partname', 'stylepack', 'standardpack', 'supplier', 'product', 'variant','usage','unit', 'price', 'tax', 'quan', 'limit']

        widgets = {
            'partno': forms.TextInput(attrs={'class': 'form-control', 'id': 'partno'}),
            'partname': forms.TextInput(attrs={'class': 'form-control', 'id': 'partname'}),
            'stylepack': forms.TextInput(attrs={'class': 'form-control', 'id': 'stylepack'}),
            'standardpack': forms.NumberInput(attrs={'class': 'form-control', 'id': 'standardpack'}),
            'supplier': forms.Select(attrs={'class': 'form-control', 'id': 'supplier'}),
            'product': forms.Select(attrs={'class': 'form-control', 'id': 'product'}),
            'unit': forms.NumberInput(attrs={'class': 'form-control', 'id': 'unit'}),
            'variant': forms.Select(attrs={'class': 'form-control', 'id': 'variant'}),
            'usage' : forms.NumberInput(attrs={'class': 'form-control', 'id': 'usage'}),
            'price' : forms.NumberInput(attrs={'class': 'form-control', 'id': 'price'}),
            'quan' : forms.NumberInput(attrs={'class': 'form-control', 'id': 'quan'}),
            'limit' : forms.NumberInput(attrs={'class': 'form-control', 'id': 'limit'}),
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
        fields = [ 'supplier', 'dimension', 'part','box', 'di_id', 'remarks','product']

        widgets = {
            'di_id': forms.NumberInput(attrs={'class': 'form-control', 'id': 'di_id', 'readonly':'readonly'}),
            'part': forms.Select(attrs={'class': 'form-control', 'id': 'part'}),
            'product': forms.Select(attrs={'class': 'form-control', 'id': 'product'}),
            'supplier': forms.Select(attrs={'class': 'form-control', 'id': 'supplier'}),
            'dimension': forms.TextInput(attrs={'class': 'form-control', 'id': 'dimension'}),
            'box': forms.NumberInput(attrs={'class': 'form-control', 'id': 'box'}),
            'remarks': forms.TextInput(attrs={'class': 'form-control', 'id': 'remarks'}),
        }