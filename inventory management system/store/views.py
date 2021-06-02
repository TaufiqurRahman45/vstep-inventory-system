from django.contrib import messages
from django.contrib.admin.models import LogEntry
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime, timedelta, date
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.pagesizes import landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.platypus.para import Paragraph
from six import BytesIO
from utils.user_log import create_log
from .filters import PartFilter
from .filters import DIFilter
from .filters import DOFilter
from .filters import POFilter

from users.models import User
from .models import (
    Supplier,
    Product,
    Order,
    Part,
    DeliveryOrder,
    DeliveryIns,
    EventManager
)
from .forms import (
    SupplierForm,
    ProductForm,
    OrderForm,
    PartForm,
    DeliveryOrderForm,
    DeliveryInsForm
)


@login_required(login_url='login')
def generate_pdf(request):
    today = date.today()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Purcahse Order.pdf"'+ today.strftime('%Y-%m-%d')
    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=landscape(letter))
    doc.title = "Purcashe Order.pdf"
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='small_text', alignment=TA_LEFT, fontName='Helvetica', borderPadding=6,
                              leading=14, fontSize=10))
    styles.add(ParagraphStyle(name='right_small_text', alignment=TA_RIGHT, fontName='Helvetica', borderPadding=6,
                              leading=14, fontSize=10))
    styles.add(ParagraphStyle(name='large_text', leading=14, fontSize=20))
    styles.add(ParagraphStyle(name='center_text', alignment=TA_CENTER, leading=14, fontSize=20))
    styles.add(ParagraphStyle(name='footer_text', leading=14, fontSize=6))
    elements = []
    paragraph_text = 'Victorious Step Sdn.Bhd. (667833-T)'
    elements.append(Paragraph(paragraph_text, styles["small_text"]))
    paragraph_text = 'No 5 Jalan Utarid U5/16,'
    elements.append(Paragraph(paragraph_text, styles["small_text"]))
    paragraph_text = '40150 Shah Alam'
    elements.append(Paragraph(paragraph_text, styles["small_text"]))
    elements.append(Paragraph('Purchase Order', styles["right_small_text"]))
    paragraph_text = 'Selangor Darul Ehsan'
    elements.append(Paragraph(paragraph_text, styles["small_text"]))
    paragraph_text = 'Tel: 03-7847 1979 / 03-7734 0205 '
    elements.append(Paragraph(paragraph_text, styles["small_text"]))
    paragraph_text = 'Fax: 03-77346310'
    elements.append(Paragraph(paragraph_text, styles["small_text"]))
    paragraph_text = 'Email: victorious.step@yahoo.com'
    elements.append(Paragraph(paragraph_text, styles["small_text"]))
    paragraph_text = 'SST No.: B16-1808-21004655'

    columns = [
        {'title': 'Supplier', 'field': 'supplier'},
    ]

    table_data = [[col['title'] for col in columns]]

    orders = Order.objects.all()
    supplier = request.GET.get('supplier')
    product = request.GET.get('product')
    if supplier:
        orders = orders.filter(supplier_id=supplier)
    if product:
        orders = orders.filter(product_id=product)

    table_row = set()
    for tr in orders:

        table_row.add(str(tr.supplier))
    table_data.append(table_row)

    table = Table(table_data, repeatRows=1, colWidths=[doc.width / 2.0] * 9)
    table.setStyle(TableStyle([
        ('BOX', (1, 1), (-2, -2), 0.70, colors.dimgrey),
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('INNERGRID', (0, 0), (-1, -1), 0.1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
    ]))
    elements.append(table)

    elements.append(Spacer(1, 50))


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
    supplier = request.GET.get('supplier')
    product = request.GET.get('product')
    if supplier:
        orders = orders.filter(supplier_id=supplier)
    if product:
        orders = orders.filter(product_id=product)
    for tr in orders:
        status = ''
        if tr.quantity <= tr.limit:
            status = 'Reorder'
        elif tr.quantity > tr.limit:
            status = 'Available'
        table_row = [str(tr.created_date.strftime("%d-%m-%Y")), tr.part.partno,
                     tr.style,tr.supplier, tr.standard, tr.quantity, tr.is_ppc, status]
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


@login_required(login_url='login')
def generate_pdf_part(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Part List.pdf"'
    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=A4,
                            rightMargin=48, leftMargin=48,
                            topMargin=100, bottomMargin=120)
    doc.title = "Part List.pdf"
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='small_text', alignment=TA_LEFT, fontName='Helvetica', borderPadding=6,
                              leading=14, fontSize=10))
    styles.add(ParagraphStyle(name='right_small_text', alignment=TA_RIGHT, fontName='Helvetica', borderPadding=6,
                              leading=14, fontSize=10))
    styles.add(ParagraphStyle(name='large_text', leading=14, fontSize=20))
    styles.add(ParagraphStyle(name='center_text', alignment=TA_CENTER, leading=14, fontSize=20))
    styles.add(ParagraphStyle(name='footer_text', leading=14, fontSize=6))

    elements = []
    paragraph_text = 'Part List'
    elements.append(Paragraph(paragraph_text, styles["large_text"]))
    elements.append(Spacer(1, 24))

    columns = [
        {'title': 'Date', 'field': 'created_date'},
        {'title': 'Part No', 'field': 'partno'},
        {'title': 'Part Name', 'field': 'partname'},
        {'title': 'Style Packeging', 'field': 'stylepack'},
        {'title': 'Standart Packeging', 'field': 'standardpack'},
        {'title': 'Unit', 'field': 'unit'},
        {'title': 'Price', 'field': 'price'},
        {'title': 'Supplier', 'field': 'supplier'},
        {'title': 'Product', 'field': 'product'},
    ]

    table_data = [[col['title'] for col in columns]]

    price = 0

    part = Part.objects.all()

    for tr in part:
        table_row = [str(tr.created_date.strftime("%d-%m-%Y")), tr.partno,
                     tr.partname, tr.stylepack, tr.standardpack, tr.unit, tr.price, tr.supplier, tr.product]
        table_data.append(table_row)
        price += tr.price
    table_data.append(['', '', 'SUBTOTAL (RM)', price])

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





@login_required(login_url='login')
def generate_pdf_do(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="DO List.pdf"'
    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=A4,
                            rightMargin=48, leftMargin=48,
                            topMargin=100, bottomMargin=120)
    doc.title = "DO List.pdf"
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='small_text', alignment=TA_LEFT, fontName='Helvetica', borderPadding=6,
                              leading=14, fontSize=10))
    styles.add(ParagraphStyle(name='right_small_text', alignment=TA_RIGHT, fontName='Helvetica', borderPadding=6,
                              leading=14, fontSize=10))
    styles.add(ParagraphStyle(name='large_text', leading=14, fontSize=20))
    styles.add(ParagraphStyle(name='center_text', alignment=TA_CENTER, leading=14, fontSize=20))
    styles.add(ParagraphStyle(name='footer_text', leading=14, fontSize=6))

    elements = []
    paragraph_text = 'DO List'
    elements.append(Paragraph(paragraph_text, styles["large_text"]))
    elements.append(Spacer(1, 24))

    columns = [
        {'title': 'Date', 'field': 'created_date'},
        {'title': 'Quantity', 'field': 'do_quantity'},
    ]

    table_data = [[col['title'] for col in columns]]

    do_quantity = 0

    deliveryorder = DeliveryOrder.objects.all()
    supplier = request.GET.get('supplier')
    if supplier:
        deliveryorder = deliveryorder.filter(supplier_id=supplier)

    for tr in deliveryorder:
        table_row = [str(tr.created_date.strftime("%d-%m-%Y")),
                     tr.do_quantity]
        table_data.append(table_row)

        do_quantity += tr.do_quantity
    table_data.append(['', '', 'SUBTOTAL (RM)', "{:.2f}".format(do_quantity)])

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

@login_required(login_url='login')
def generate_pdf_di(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Delivery Instruction.pdf"'
    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=A4,
                            rightMargin=48, leftMargin=48,
                            topMargin=100, bottomMargin=120)
    doc.title = "Delivery Instruction.pdf"
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='small_text', alignment=TA_LEFT, fontName='Helvetica', borderPadding=6,
                              leading=14, fontSize=10))
    styles.add(ParagraphStyle(name='right_small_text', alignment=TA_RIGHT, fontName='Helvetica', borderPadding=6,
                              leading=14, fontSize=10))
    styles.add(ParagraphStyle(name='large_text', leading=14, fontSize=20))
    styles.add(ParagraphStyle(name='center_text', alignment=TA_CENTER, leading=14, fontSize=20))
    styles.add(ParagraphStyle(name='footer_text', leading=14, fontSize=6))

    elements = []
    paragraph_text = 'Delivery Instruction'
    elements.append(Paragraph(paragraph_text, styles["large_text"]))
    elements.append(Spacer(1, 24))

    columns = [
        {'title': 'Date', 'field': 'created_date'},
        {'title': 'Variant', 'field': 'variant'},
        {'title': 'Usage', 'field': 'usage'},
        {'title': 'Part', 'field': 'part'},
        {'title': 'Supplier', 'field': 'supplier'},
        {'title': 'Dimension', 'field': 'dimension'},
        {'title': 'Box/Qty', 'field': 'box'},
        {'title': 'Remarks', 'field': 'remarks'},
        
    ]

    table_data = [[col['title'] for col in columns]]

    box = 0

    deliveryins = DeliveryIns.objects.all()
    supplier = request.GET.get('supplier')
    if supplier:
        deliveryins = deliveryins.filter(supplier_id=supplier)

    for tr in deliveryins:
        table_row = [str(tr.created_date.strftime("%d-%m-%Y")),
                     tr.variant, tr.usage, tr.order.part.partno, tr.supplier, tr.dimension, tr.box, tr.remarks] 
        table_data.append(table_row)

        box += tr.box
    table_data.append(['', '', 'SUBTOTAL (RM)', "{:.2f}".format(box)])

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
            address2 = forms.cleaned_data['address2']
            address3 = forms.cleaned_data['address3']
            postcode = forms.cleaned_data['postcode']
            email = forms.cleaned_data['email']
            phone = forms.cleaned_data['phone']
            supplier = Supplier.objects.create(name=name, email=email, address=address, address2=address2, address3=address3,
                                               postcode=postcode, phone=phone)
            create_log(request, supplier)
        return redirect('supplier-list')
    context = {
        'form': forms
    }
    return render(request, 'store/addSupplier.html', context)


class SupplierListView(ListView):
    model = Supplier
    template_name = 'store/supplier_list.html'

    # context_object_name = 'supplier'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['supplier'] = Supplier.objects.all().order_by('-id')
        return context


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

    # context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = Product.objects.all().order_by('-id')
        return context


# Order views
@login_required(login_url='login')
def create_order(request):
    from django import forms
    form = OrderForm()
    form.fields['is_ppc'].queryset = User.objects.filter(is_ppc=True)
    # form.fields['new_stock'].widget = forms.HiddenInput()

    if request.method == 'POST':
        forms = OrderForm(request.POST)
        if forms.is_valid():
            supplier = forms.cleaned_data['supplier']
            product = forms.cleaned_data['product']
            part = forms.cleaned_data['part']
            style = forms.cleaned_data['style']
            quantity = forms.cleaned_data['quantity']
            standard = forms.cleaned_data['standard']
            limit = forms.cleaned_data['limit']
            is_ppc = forms.cleaned_data['is_ppc']
            tax = forms.cleaned_data['tax']
            price = forms.cleaned_data['price']
            unit = forms.cleaned_data['unit']

            order = Order.objects.create(
                supplier=supplier,
                product=product,
                part=part,
                style=style,
                standard=standard,
                quantity=quantity,
                limit=limit,
                is_ppc=is_ppc,
                tax=tax,
                price=price,
                unit=unit,
                terms=30,
                remarks='Follow DI',

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
    context_object_name = 'order'

    def get_queryset(self):
        queryset = self.model.objects.all().order_by('-id')
        if self.request.GET.get('supplier'):
            queryset = queryset.filter(supplier_id=self.request.GET.get('supplier'))
        elif self.request.GET.get('product'):
            queryset = queryset.filter(product_id=self.request.GET.get('product'))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = POFilter(self.request.GET, queryset=self.get_queryset())
        return context


@login_required(login_url='login')
def create_part(request):
    from django import forms
    form = PartForm()

    if request.method == 'POST':
        forms = PartForm(request.POST)
        if forms.is_valid():
            supplier = forms.cleaned_data['supplier']
            product = forms.cleaned_data['product']
            partno = forms.cleaned_data['partno']
            partname = forms.cleaned_data['partname']
            stylepack = forms.cleaned_data['stylepack']
            standardpack = forms.cleaned_data['standardpack']
            unit = forms.cleaned_data['unit']
            price = forms.cleaned_data['price']
            tax = forms.cleaned_data['tax']

            part = Part.objects.create(
                supplier=supplier,
                product=product,
                partno=partno,
                partname=partname,
                stylepack=stylepack,
                standardpack=standardpack,
                unit=unit,
                price=price,
                tax=tax,
            )
            create_log(request, part)
            return redirect('part-list')
    context = {
        'form': form
    }
    return render(request, 'store/addPart.html', context)


class PartListView(ListView):
    model = Part
    template_name = 'store/part_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['part'] = Part.objects.all().order_by('-id')
        context['filter'] = PartFilter(self.request.GET, queryset=self.get_queryset())
        return context


@login_required(login_url="/login")
def updatePart(request, pk):
    action = 'update'
    part = Part.objects.get(id=pk)
    form = PartForm(instance=part)

    if request.method == 'POST':
        form = PartForm(request.POST, instance=part)
        if form.is_valid():
            form.save()
            return redirect('part-list')

    context = {'action': action, 'form': form}
    return render(request, 'store/update_part.html', context)


def deletePart(request, pk):
    part = Part.objects.get(id=pk)
    if request.method == 'POST':
        part_id = part.partname
        part.delete()
        return redirect('part-list')

    return render(request, 'store/delete_part.html', {'item': part})


@login_required(login_url='login')
def create_deliveryorder(request):
    form = DeliveryOrderForm()

    if request.method == 'POST':
        forms = DeliveryOrderForm(request.POST)
        if forms.is_valid():
            supplier = forms.cleaned_data['supplier']
            do_quantity = forms.cleaned_data['do_quantity']
            order = forms.cleaned_data['order']

            o = Order.objects.get(id=order.id)
            if do_quantity > o.quantity:
                messages.warning(request, "Quantity can't be greater than order quantity")
                return redirect('do-list')

            deliveryorder = DeliveryOrder.objects.create(
                supplier=supplier,
                do_quantity=do_quantity,
                order=order,
            )
            o.quantity -= do_quantity  # deduct quantity
            o.save()
            messages.success(request, "Delivery order created successfully")
            create_log(request, deliveryorder)
            return redirect('do-list')
    context = {
        'form': form
    }
    return render(request, 'store/addDo.html', context)


class DeliveryOrderListView(ListView):
    model = DeliveryOrder
    template_name = 'store/do_list.html'
    context_object_name = 'deliveryorder'

    def get_queryset(self):
        queryset = self.model.objects.all().order_by('-id')
        if self.request.GET.get('supplier'):
            queryset = queryset.filter(supplier_id=self.request.GET.get('supplier'))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = DOFilter(self.request.GET, queryset=self.get_queryset())
        return context


@login_required(login_url='login')
def create_deliveryins(request):
    from django import forms
    form = DeliveryInsForm()

    if request.method == 'POST':
        forms = DeliveryInsForm(request.POST)
        if forms.is_valid():
            variant = forms.cleaned_data['variant']
            usage = forms.cleaned_data['usage']
            order = forms.cleaned_data['order']
            supplier = forms.cleaned_data['supplier']
            dimension = forms.cleaned_data['dimension']
            box = forms.cleaned_data['box']
            remarks = forms.cleaned_data['remarks']

            deliveryins = DeliveryIns.objects.create(
                variant=variant,
                usage=usage,
                order=order,
                supplier=supplier,
                dimension=dimension,
                box=box,
                remarks=remarks,
            )
            create_log(request, deliveryins)
            return redirect('dins-list')
    context = {
        'form': form
    }
    return render(request, 'store/addDins.html', context)


class DeliveryInsListView(ListView):
    model = DeliveryIns
    template_name = 'store/dins-list.html'
    context_object_name = 'deliveryins'

    def get_queryset(self):
        queryset = self.model.objects.all().order_by('-id')
        if self.request.GET.get('supplier'):
            queryset = queryset.filter(supplier_id=self.request.GET.get('supplier'))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = DIFilter(self.request.GET, queryset=self.get_queryset())
        DeliveryIns._base_manager.filter(created_date__lt=timezone.now() - timezone.timedelta(days=1)).delete()
        return context

@login_required(login_url="/login")
def updateDI(request, pk):
    action = 'update'
    deliveryins = DeliveryIns.objects.get(id=pk)
    form = DeliveryInsForm(instance=deliveryins)

    if request.method == 'POST':
        form = DeliveryInsForm(request.POST, instance=deliveryins)
        if form.is_valid():
            form.save()
            return redirect('dins-list')

    context = {'action': action, 'form': form}
    return render(request, 'store/update_dins.html', context)


def deleteDI(request, pk):
    deliveryins = DeliveryIns.objects.get(id=pk)
    if request.method == 'POST':
        deliveryins_id = deliveryins.order
        deliveryins.delete()
        return redirect('dins-list')

    return render(request, 'store/delete_dins.html', {'item': deliveryins})


@login_required(login_url="/login")
def updateDO(request, pk):
    action = 'update'
    deliveryorder = DeliveryOrder.objects.get(id=pk)
    previous_do = deliveryorder.do_quantity
    form = DeliveryOrderForm(instance=deliveryorder)

    if request.method == 'POST':
        form = DeliveryOrderForm(request.POST, instance=deliveryorder)
        if form.is_valid():
            do = form.save()
            create_log(request, do, object_repr=do.order.part.partname,
                       change_message=f"do_quantity {previous_do} to {do.do_quantity}")
            return redirect('do-list')

    context = {'action': action, 'form': form}
    return render(request, 'store/update_do.html', context)


def deleteDO(request, pk):
    deliveryorder = DeliveryOrder.objects.get(id=pk)
    if request.method == 'POST':
        deliveryorder_id = deliveryorder.part
        deliveryorder.delete()
        return redirect('do-list')

    return render(request, 'store/delete_do.html', {'item': deliveryorder})


@login_required(login_url='login')
def update_Order(request):
    return render(request, 'store/updateOrder.html')


@login_required(login_url="/login")
def updateOrder(request, pk):
    action = 'update'
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order, initial={'new_stock': 0})

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            order = form.save()
            try:
                order.quantity += order.new_stock
                order.save()
            except:
                pass
            if order.quantity <= order.limit:
                from django.core.mail import EmailMessage

                # to = order.is_ppc.email
                to = "toufiqurrahman45@gmail.com"

                msg = EmailMessage(subject="Status: Reorder", from_email="Webmaster@victoriousstep.com",
                                   to=[to])
                msg.template_name = 'REORDER'
                msg.template_content = {
                    'ORDER_ID': order.id,
                    'PRODUCT_ID': order.product_id,
                }
                msg.send(fail_silently=True)
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
