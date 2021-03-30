from django.contrib.admin.models import LogEntry
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.platypus.para import Paragraph
from six import BytesIO
from utils.user_log import create_log

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


@login_required(login_url='login')
def generate_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Order List.pdf"'
    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=A4,
                            rightMargin=48, leftMargin=48,
                            topMargin=100, bottomMargin=120)
    doc.title = "Order List.pdf"
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='small_text', alignment=TA_LEFT, fontName='Helvetica', borderPadding=6,
                              leading=14, fontSize=10))
    styles.add(ParagraphStyle(name='right_small_text', alignment=TA_RIGHT, fontName='Helvetica', borderPadding=6,
                              leading=14, fontSize=10))
    styles.add(ParagraphStyle(name='large_text', leading=14, fontSize=20))
    styles.add(ParagraphStyle(name='center_text', alignment=TA_CENTER, leading=14, fontSize=20))
    styles.add(ParagraphStyle(name='footer_text', leading=14, fontSize=6))

    elements = []
    paragraph_text = 'Order List'
    elements.append(Paragraph(paragraph_text, styles["large_text"]))
    elements.append(Spacer(1, 24))

    columns = [
        {'title': 'Date', 'field': 'created_date'},
        {'title': 'Part No', 'field': 'partno'},
        {'title': 'Style Packaging', 'field': 'style'},
        {'title': 'Standard', 'field': 'standard'},
        {'title': 'Quantity PCS', 'field': 'quantity'},
        {'title': 'PIC', 'field': 'is_ppc'},
        {'title': 'Status', 'field': 'limit'},
    ]

    table_data = [[col['title'] for col in columns]]

    orders = Order.objects.all()
    for tr in orders:
        status = ''
        if tr.quantity < tr.limit:
            status = 'Reorder'
        elif tr.quantity > tr.limit:
            status = 'Available'
        table_row = [str(tr.created_date.strftime("%d-%m-%Y")), tr.partno,
                     tr.style, tr.standard, tr.quantity, tr.is_ppc, status]
        table_data.append(table_row)

    table = Table(table_data, repeatRows=1, colWidths=[doc.width / 7.0] * 7)
    table.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 0.20, colors.dimgrey),
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('INNERGRID', (0, 0), (-1, -1), 0.1, colors.black),
        # ('SIZE', (0, 0), (-1, -1), 6.5),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        # ('SPAN', (0, 0), (3, 0))
    ]))
    elements.append(table)

    elements.append(Spacer(1, 50))

    doc.build(elements)

    pdf = pdf_buffer.getvalue()
    pdf_buffer.close()
    response.write(pdf)

    return response


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
            supplier = Supplier.objects.create(name=name, email=email, address=address)
            create_log(request, supplier)
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
            product = forms.save()
            create_log(request, product)
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
    from django import forms
    form = OrderForm()
    form.fields['is_ppc'].queryset = User.objects.filter(is_ppc=True)
    form.fields['new_stock'].widget = forms.HiddenInput()

    if request.method == 'POST':
        forms = OrderForm(request.POST)
        if forms.is_valid():
            supplier = forms.cleaned_data['supplier']
            product = forms.cleaned_data['product']
            partno = forms.cleaned_data['partno']
            description = forms.cleaned_data['description']
            style = forms.cleaned_data['style']
            quantity = forms.cleaned_data['quantity']
            standard = forms.cleaned_data['standard']
            limit = forms.cleaned_data['limit']
            is_ppc = forms.cleaned_data['is_ppc']
            new_stock = forms.cleaned_data['new_stock']

            order = Order.objects.create(
                supplier=supplier,
                product=product,
                partno=partno,
                description=description,
                style=style,
                standard=standard,
                quantity=quantity,
                limit=limit,
                is_ppc=is_ppc,
                new_stock=new_stock,
            )
            create_log(request, order)
            return redirect('order-list')
    context = {
        'form': form
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
            order = form.save()
            order.quantity += order.new_stock
            order.save()
            create_log(request, order)
            return redirect('order-list')

    context = {'action': action, 'form': form}
    return render(request, 'store/update_order.html', context)


@login_required(login_url="/login")
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order_id = order.partno
        order.delete()
        create_log(request, order, 3)
        return redirect('order-list')

    return render(request, 'store/delete.html', {'item': order})


@login_required(login_url='/login')
def logs(request):
    my_logs = LogEntry.objects.all()
    return render(request, 'store/logs.html', {'logs': my_logs})
