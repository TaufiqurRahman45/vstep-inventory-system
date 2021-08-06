from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import F

from store.models import Product,Part, Supplier, Order


@login_required(login_url='login')
def dashboard(request):
    total_product = Product.objects.count()
    total_supplier = Supplier.objects.count()
    total_oder = Order.objects.count()
    parts = Part.objects.filter(quan__lte=F('limit')).order_by('-id')
    
    context = {
        'product': total_product,
        'supplier': total_supplier,
        'order': total_oder,
        'parts': parts,
    }
    return render(request, 'dashboard.html', context)
