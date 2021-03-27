from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from store.models import Product, Supplier, Order


@login_required(login_url='login')
def dashboard(request):
    total_product = Product.objects.count()
    total_supplier = Supplier.objects.count()
    total_oder = Order.objects.count()
    orders = Order.objects.all().order_by('-id')
    context = {
        'product': total_product,
        'supplier': total_supplier,
        'order': total_oder,
        'orders': orders
    }
    return render(request, 'dashboard.html', context)
