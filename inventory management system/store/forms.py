from django import forms

from .models import Season, Drop, Product, Order, Delivery


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
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'username',
        'data-val': 'true',
        'data-val-required': 'Please enter username',
    }))
    # password = forms.CharField(widget=forms.PasswordInput(attrs={
    #     'class': 'form-control',
    #     'id': 'password',
    #     'data-val': 'true',
    #     'data-val-required': 'Please enter password',
    # }))
    # retype_password = forms.CharField(widget=forms.PasswordInput(attrs={
    #     'class': 'form-control',
    #     'id': 'retype_password',
    #     'data-val': 'true',
    #     'data-val-required': 'Please enter retype_password',
    # }))

class SeasonForm(forms.ModelForm):
    class Meta:
        model = Season
        fields = ['name', 'description']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'name'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'id': 'description'})
        }


class DropForm(forms.ModelForm):
    class Meta:
        model = Drop
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'name'})
        }



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
        fields = ['supplier', 'product', 'partno', 'description', 'style', 'standard', 'quantity', 'limit', 'is_ppc']

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
        }


class DeliveryForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = '__all__'

        widgets = {
            'order': forms.Select(attrs={'class': 'form-control', 'id': 'order'}),
            'courier_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'courier_name'}),
        }

class PurchaseUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("limit", "new_stock")
