from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required

from users.models import User
from .models import (
    Supplier,
    Product,
    Order,
)
from .forms import (
    SupplierForm,
    ProductForm,
    OrderForm,
)

# Supplier views
@login_required(login_url='login')
def create_supplier(request):
    forms = SupplierForm()
    if request.method == 'POST':
        forms = SupplierForm(request.POST)
        if forms.is_valid():
            name = forms.cleaned_data['name']
            address = forms.cleaned_data['address']
            email = forms.cleaned_data['email']
            Supplier.objects.create( name=name, email=email, address=address)
        return redirect('supplier-list')
    context = {
        'form': forms
    }
    return render(request, 'store/addSupplier.html', context)


class SupplierListView(ListView):
    model = Supplier
    template_name = 'store/supplier_list.html'
    context_object_name = 'supplier'


# Product views
@login_required(login_url='login')
def create_product(request):
    forms = ProductForm()
    if request.method == 'POST':
        forms = ProductForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('product-list')
    context = {
        'form': forms
    }
    return render(request, 'store/addProduct.html', context)

class ProductListView(ListView):
    model = Product
    template_name = 'store/product_list.html'
    context_object_name = 'product'


# Order views
@login_required(login_url='login')
def create_order(request):
    forms = OrderForm()
    
    if request.method == 'POST':
        forms = OrderForm(request.POST)
        if forms.is_valid():
            supplier = forms.cleaned_data['supplier']
            product = forms.cleaned_data['product']
            partno = forms.cleaned_data['partno']
            description = forms.cleaned_data['description']
            style = forms.cleaned_data['style']
            quantity = forms.cleaned_data['quantity']
            standard =forms.cleaned_data['standard']
            limit = forms.cleaned_data['limit']
            is_ppc = forms.cleaned_data['is_ppc']
            new_stock = forms.cleaned_data['new_stock']
            
            Order.objects.create(
                supplier=supplier,
                product=product,
                partno=partno,
                description=description,
                style=style,
                standard=standard,
                quantity=quantity,
                limit=limit,
                is_ppc=is_ppc, 
                new_stock = new_stock,
               
            )
            return redirect('order-list')
    context = {
        'form': forms
    }
    return render(request, 'store/addOrder.html', context)


class OrderListView(ListView):
    model = Order
    template_name = 'store/order_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = Order.objects.all().order_by('-id')
        return context

@login_required(login_url='login')
def update_Order(request):

    return render(request, 'store/updateOrder.html')


@login_required(login_url="/login")
def updateOrder(request, pk):
	action = 'update'
	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)

	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('order-list')

	context =  {'action':action, 'form':form}
	return render(request, 'store/update_order.html', context)

@login_required(login_url="/login")
def deleteOrder(request, pk):
	order = Order.objects.get(id=pk)
	if request.method == 'POST':
		order_id = order.partno
		order.delete()
		return redirect('order-list')
		
	return render(request, 'store/delete.html', {'item':order})