import random
import string
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
from reportlab.lib.pagesizes import letter,A4
from reportlab.lib.pagesizes import landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.platypus.para import Paragraph
from reportlab.lib.units import mm, inch
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
    # EventManager
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
    pagesize = (15 * inch, 10 * inch)
    doc = SimpleDocTemplate(pdf_buffer, pagesize=pagesize)
    doc.title = "Purcashe Order.pdf"
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='small_text', alignment=TA_LEFT, fontName='Times-Roman', borderPadding=6,
                              leading=16, fontSize=13))
    styles.add(ParagraphStyle(name='right_small_text', alignment=TA_RIGHT, fontName='Helvetica', borderPadding=6,
                              leading=14, fontSize=12))
    styles.add(ParagraphStyle(name='large_text', leading=14, fontSize=15, spaceAfter = 12, spaceBefore = 10))
    styles.add(ParagraphStyle(name='center_text', alignment=TA_CENTER, leading=14, fontSize=20))
    styles.add(ParagraphStyle(name='footer_text', leading=14, fontSize=6))
    elements = []
    elements.append(Paragraph('Inovice Number: PO {}'.format("A"+ str(random.randint(1000, 2000))), styles["right_small_text"]))

    elements.append(Paragraph('Purchase Order', styles["right_small_text"]))
    elements.append(Paragraph('Date: {}'.format(str(datetime.now().date().strftime("%d-%m-%Y"))), styles["right_small_text"]))
    paragraph_text = 'Victorious Step Sdn.Bhd. (667833-T)'
    elements.append(Paragraph(paragraph_text, styles["small_text"]))
    paragraph_text = 'No 5 Jalan Utarid U5/16,'
    elements.append(Paragraph(paragraph_text, styles["small_text"]))
    paragraph_text = '40150 Shah Alam'
    elements.append(Paragraph(paragraph_text, styles["small_text"]))
    paragraph_text = 'Selangor Darul Ehsan'
    elements.append(Paragraph(paragraph_text, styles["small_text"]))
    paragraph_text = 'Tel: 03-7847 1979 / 03-7734 0205 '
    elements.append(Paragraph(paragraph_text, styles["small_text"]))
    paragraph_text = 'Fax: 03-77346310'
    elements.append(Paragraph(paragraph_text, styles["small_text"]))
    paragraph_text = 'Email: victorious.step@yahoo.com'
    elements.append(Paragraph(paragraph_text, styles["small_text"]))
    paragraph_text = 'SST No.: B16-1808-21004655'

    elements.append(Paragraph(paragraph_text, styles["small_text"]))
    paragraph_text = u"<b>Supplier: </b>"
    elements.append(Paragraph(paragraph_text, styles["large_text"]))

    table_data = []

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

# address 1
    table_add = set()
    for tr in orders:

        table_add.add(str(tr.supplier.address))
        
    table_data.append(table_add)

# address 2
    table_add2 = set()
    for tr in orders:

        table_add2.add(str(tr.supplier.address2))
        
    table_data.append(table_add2)

# address 3
    table_add3 = set()
    for tr in orders:

        table_add3.add(str(tr.supplier.address3))
    
    table_data.append(table_add3)

# phone
    table_phn = set()
    for tr in orders:

        table_phn.add(str(tr.supplier.phone))
        
    table_data.append(table_phn)

    table = Table(table_data, repeatRows=0,  colWidths=None)
    
    table.hAlign = "LEFT"
    
    elements.append(table)

    elements.append(Spacer(5, 5))


# Prod
    columns = [
            {'title': 'Payment Terms', 'field': 'terms'},
            {'title': 'Model', 'field': 'product'},
            {'title': 'Remarks', 'field': 'remarks'},
        ]

    table_data = [[col['title'] for col in columns]]

    orders = Order.objects.all()
    supplier = request.GET.get('supplier')
    product = request.GET.get('product')
    if supplier:
        orders = orders.filter(supplier_id=supplier)
    if product:
        orders = orders.filter(product_id=product)

    table_sec = set()
    for tr in orders:
        table_sec=[str(tr.terms), tr.product, tr.remarks]
    table_data.append(table_sec)
    table = Table(table_data, repeatRows=1, colWidths=[doc.width / 7.0] * 7)
    table.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 0.20, colors.dimgrey),
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('INNERGRID', (0, 0), (-1, -1), 0.1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
    ]))
    elements.append(table)

    elements.append(Spacer(1, 50))

#end prod

    columns = [
        {'title': 'Part No', 'field': 'partno'},
        {'title': 'Part Name', 'field': 'partname'},
        {'title': 'Style P', 'field': 'style'},
        {'title': 'Standard P', 'field': 'standardpack'},
        {'title': 'Unit Per Car', 'field': 'unit'},
        {'title': 'Quantity PCS', 'field': 'quantity'},
        {'title': 'Tax', 'field': 'tax'},
        {'title': 'Unit Price', 'field': 'price'},
        {'title': 'Amount', 'field': 'amount'},
    ]

    table_data = [[col['title'] for col in columns]]
    table_data1 = []
    orders = Order.objects.all()
    
    amount = 0
    for tr in orders:
        table_row = [str(tr.part.partno),tr.part.partname,
                    tr.part.stylepack, tr.part.standardpack,tr.part.unit, tr.quantity, tr.part.tax, tr.part.price, tr.amount]      
        table_data.append(table_row)

        amount += tr.amount
    table_data1.append(['','','','','','','', 'GRAND TOTAL (RM)','', amount])
    
    table = Table(table_data, colWidths=[1.5*inch,4.5*inch,1*inch,1*inch, 1.5*inch,1.5*inch, 0.8*inch])
    table.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 0.20, colors.dimgrey),
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('INNERGRID', (0, 0), (-1, -1), 0.1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
    ]))
    elements.append(table)

    table1 = Table(table_data1, colWidths=[1.4*inch])
    table1.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
    ]))
    elements.append(table1)
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
    today = date.today()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Delivery Order.pdf"'+ today.strftime('%Y-%m-%d')
    pdf_buffer = BytesIO()
    pagesize = (15 * inch, 10 * inch)
    doc = SimpleDocTemplate(pdf_buffer, pagesize=pagesize)
    doc.title = "Delivery Order.pdf"
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='small_text', alignment=TA_LEFT, fontName='Times-Roman', borderPadding=6,
                              leading=16, fontSize=13))
    styles.add(ParagraphStyle(name='right_small_text', alignment=TA_RIGHT, fontName='Helvetica', borderPadding=6,
                              leading=14, fontSize=12))
    styles.add(ParagraphStyle(name='large_text', leading=14, fontSize=15, spaceAfter = 12, spaceBefore = 10))
    styles.add(ParagraphStyle(name='center_text', alignment=TA_CENTER, leading=14, fontSize=20))
    styles.add(ParagraphStyle(name='footer_text', leading=14, fontSize=6))
    elements = []
    elements.append(Paragraph('No: DO {}'.format(str(random.randint(1000, 2000))), styles["right_small_text"]))

    elements.append(Paragraph('Delivery Order', styles["right_small_text"]))
    elements.append(Paragraph('Date: {}'.format(str(datetime.now().date().strftime("%d-%m-%Y"))), styles["right_small_text"]))
    paragraph_text = 'Victorious Step Sdn.Bhd. (667833-T)'
    elements.append(Paragraph(paragraph_text, styles["small_text"]))
    paragraph_text = 'No 5 Jalan Utarid U5/16,'
    elements.append(Paragraph(paragraph_text, styles["small_text"]))
    paragraph_text = '40150 Shah Alam'
    elements.append(Paragraph(paragraph_text, styles["small_text"]))
    paragraph_text = 'Selangor Darul Ehsan'
    elements.append(Paragraph(paragraph_text, styles["small_text"]))
    paragraph_text = 'Tel: 03-7847 1979 / 03-7734 0205 '
    elements.append(Paragraph(paragraph_text, styles["small_text"]))
    paragraph_text = 'Fax: 03-77346310'
    elements.append(Paragraph(paragraph_text, styles["small_text"]))
    paragraph_text = 'Email: victorious.step@yahoo.com'
    elements.append(Paragraph(paragraph_text, styles["small_text"]))
    paragraph_text = 'SST No.: B16-1808-21004655'

    elements.append(Paragraph(paragraph_text, styles["small_text"]))
    paragraph_text = 'To'
    elements.append(Paragraph(paragraph_text, styles["large_text"]))
    paragraph_text = u"<b>PROTON TG MALIM SDN BHD  </b>"

    elements.append(Paragraph(paragraph_text, styles["small_text"]))
    paragraph_text = 'JABATAN TRIM & FINAL'

    elements.append(Paragraph(paragraph_text, styles["small_text"]))
    paragraph_text = 'MUKIM HULLU BERNAM TIMUR'

    elements.append(Paragraph(paragraph_text, styles["small_text"]))
    paragraph_text = 'DAERAH MUALLIM'

    elements.append(Paragraph(paragraph_text, styles["small_text"]))
    paragraph_text = '35950, TANJONG MALIM'

    elements.append(Paragraph(paragraph_text, styles["small_text"]))
    paragraph_text = 'PERAK DARUL RIDZUAN'

    elements.append(Paragraph(paragraph_text, styles["small_text"]))

    # table_data = []

    columns = [
        {'title': 'Part No', 'field': 'partno'},
        {'title': 'Part Name', 'field': 'partname'},
        {'title': 'Quantity DO', 'field': 'do_quantity'},
        {'title': 'Quantity PO', 'field': 'order'},
    ]

    table_data = [[col['title'] for col in columns]]
    do = DeliveryOrder.objects.all()
    
    for tr in do:
        table_row = [str(tr.order.part.partno),tr.order,
                    tr.do_quantity, tr.order.quantity]      
        table_data.append(table_row)
    
    table = Table(table_data, colWidths=[1.5*inch,4.5*inch,1.5*inch,1.5*inch,], spaceBefore=10)
    table.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 0.20, colors.dimgrey),
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('INNERGRID', (0, 0), (-1, -1), 0.1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
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
    today = date.today()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Delivery Instructions.pdf"'+ today.strftime('%Y-%m-%d')
    pdf_buffer = BytesIO()
    pagesize = (15 * inch, 10 * inch)
    doc = SimpleDocTemplate(pdf_buffer, pagesize=pagesize)
    doc.title = "Delivery Instructions.pdf"
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='small_text', alignment=TA_LEFT, fontName='Times-Roman', borderPadding=6,
                              leading=16, fontSize=13))
    styles.add(ParagraphStyle(name='right_small_text', alignment=TA_RIGHT, fontName='Helvetica', borderPadding=6,
                              leading=14, fontSize=12))
    styles.add(ParagraphStyle(name='large_text', leading=14, fontSize=15, spaceAfter = 12, spaceBefore = 10))
    styles.add(ParagraphStyle(name='center_text', alignment=TA_CENTER, leading=14, fontSize=20))
    styles.add(ParagraphStyle(name='footer_text', leading=14, fontSize=6))
    elements = []
    elements.append(Paragraph('Number: DI {}'.format(str(random.randint(1000, 2000))), styles["right_small_text"]))

    elements.append(Paragraph('Delivery Instructions', styles["right_small_text"]))
    elements.append(Paragraph('Date: {}'.format(str(datetime.now().date().strftime("%d-%m-%Y"))), styles["right_small_text"]))
    paragraph_text = 'Victorious Step Sdn.Bhd. (667833-T)'
    elements.append(Paragraph(paragraph_text, styles["small_text"]))
    paragraph_text = 'No 5 Jalan Utarid U5/16,'
    elements.append(Paragraph(paragraph_text, styles["small_text"]))
    paragraph_text = '40150 Shah Alam'
    elements.append(Paragraph(paragraph_text, styles["small_text"]))
    paragraph_text = 'Selangor Darul Ehsan'
    elements.append(Paragraph(paragraph_text, styles["small_text"]))
    paragraph_text = 'Tel: 03-7847 1979 / 03-7734 0205 '
    elements.append(Paragraph(paragraph_text, styles["small_text"]))
    paragraph_text = 'Fax: 03-77346310'
    elements.append(Paragraph(paragraph_text, styles["small_text"]))
    paragraph_text = 'Email: victorious.step@yahoo.com'
    elements.append(Paragraph(paragraph_text, styles["small_text"]))
    paragraph_text = 'SST No.: B16-1808-21004655'
    elements.append(Paragraph(paragraph_text, styles["small_text"]))

    columns = [
        {'title': 'Variant', 'field': 'variant'},
        {'title': 'Usage', 'field': 'usage'},
        {'title': 'Part No', 'field': 'partno'},
        {'title': 'Part Name', 'field': 'order'},
        {'title': 'Supplier', 'field': 'supplier'},
        {'title': 'Dimension P', 'field': 'dimension'},
        {'title': 'QTY/BOX', 'field': 'box'},
    ]
    table_data = [[col['title'] for col in columns]]
    din = DeliveryIns.objects.all()

    supplier = request.GET.get('supplier')
    product = request.GET.get('product')
    if supplier:
        din = din.filter(supplier_id=supplier)
    if product:
        din = din.filter(product_id=product)
    
    for tr in din:
        table_row = [str(tr.variant),tr.usage,
                    tr.order.part.partno, tr.order, tr.supplier, tr.dimension, tr.box]      
        table_data.append(table_row)

    columns = [
            
            {'title': 'Model', 'field': 'product'},
        ]

    table_data1 = [[col['title'] for col in columns]]

    orders = Order.objects.all()
    supplier = request.GET.get('supplier')
    product = request.GET.get('product')
    if supplier:
        orders = orders.filter(supplier_id=supplier)
    if product:
        orders = orders.filter(product_id=product)

    table_sec = set()
    for tr in orders:
        table_sec=[str(tr.product)]
    table_data1.append(table_sec)

    table = Table(table_data1, repeatRows=1, colWidths=[doc.width / 7.0] * 7)
    table.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 0.20, colors.dimgrey),
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('INNERGRID', (0, 0), (-1, -1), 0.1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
    ]))
    elements.append(table)

    elements.append(Spacer(1, 50))
    
    table = Table(table_data, colWidths=[1*inch,0.7*inch,1.5*inch,4.5*inch,3*inch,1.5*inch, 0.8*inch], spaceBefore=10)
    table.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 0.20, colors.dimgrey),
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('INNERGRID', (0, 0), (-1, -1), 0.1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
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
            # create_log(request, supplier)
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
            # create_log(request, product)
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

def random_string():
    return str(random.randint(10000, 99999))

# Order views
@login_required(login_url='login')
def create_order(request):
    from django import forms
    form = OrderForm()
    form.fields['is_ppc'].queryset = User.objects.filter(is_ppc=True)
    form.fields['new_stock'].widget = forms.HiddenInput()

    if request.method == 'POST':
        a = []
        max_l = 0
        for k, v in dict(request.POST.lists()).items():
            if type(v) == list:
                max_l = max(max_l, len(v))
                a.append([(k, x) for x in v])
            else:
                a.append((k, v))

        forms_data = [dict() for _ in range(max_l)]
        for e in a:
            if len(e) == 1:
                k, v = e[0]
                for d in forms_data:
                    d[k] = v
            else:
                assert len(e) == max_l
                for d, ee in zip(forms_data, e):
                    k, v = ee
                    d[k] = v

        for form_data in forms_data:
            forms = OrderForm(form_data)
            if forms.is_valid():
                po_id = forms.cleaned_data['po_id']
                supplier = forms.cleaned_data['supplier']
                product = forms.cleaned_data['product']
                part = forms.cleaned_data['part']
                quantity = forms.cleaned_data['quantity']
                is_ppc = forms.cleaned_data['is_ppc']
                new_stock = forms.cleaned_data['new_stock']
                created_date = forms.cleaned_data['created_date']

                q = Part.objects.get(id=part.id)

                order = Order.objects.create(
                    po_id=po_id,
                    supplier=supplier,
                    product=product,
                    part=part,
                    quantity=quantity,
                    is_ppc=is_ppc,
                    terms=30,
                    remarks='Follow DI',
                    new_stock=new_stock,
                    created_date=created_date,
                )

                q.quan += quantity  # deduct quantity
                q.save()

                # create_log(request, order)
        return redirect('order-list')
    context = {
        'form': form
    }
    return render(request, 'store/addOrder.html', context)

# Dependent/Chained Dropdown
def load_parts(request):
    supplier_id = request.GET.get('supplier')
    parts = Part.objects.filter(supplier_id=supplier_id).order_by('partname')
    return render(request, 'store/part_dropdown_list_options.html', {'parts': parts})

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
            part = form.cleaned_data['part']
            quantity = form.cleaned_data['quantity']

            q = Part.objects.get(id=part.id)
            q.quan += quantity  # add quantity
            q.save()
            PO = form.save()
            return redirect('order-list')

    context = {'action': action, 'form': form}
    return render(request, 'store/update_order.html', context)


@login_required(login_url="/login")
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order_id = order.part.partno
        order.delete()
        create_log(request, order, 3)
        return redirect('order-list')

    return render(request, 'store/delete.html', {'item': order})


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
            quan = forms.cleaned_data['quan']
            limit = forms.cleaned_data['limit']

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
                quan=quan,
                limit=limit,
            )
            # create_log(request, part)
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

            if part.quan <= part.limit:
                from django.core.mail import EmailMessage

                # to = order.is_ppc.email
                to = "toufiqurrahman45@gmail.com"

                msg = EmailMessage(subject="Status: Reorder", from_email="Webmaster@victoriousstep.com",
                                   to=[to])
                msg.template_name = 'REORDER'
                msg.template_content = {
                    'PART_NO': part.partno,
                    'PART_NAME': part.partname,
                    'AVAILABLE STOCK': part.quan,
                }
                msg.send(fail_silently=True)
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
        a = []
        max_l = 0
        for k, v in dict(request.POST.lists()).items():
            if type(v) == list:
                max_l = max(max_l, len(v))
                a.append([(k, x) for x in v])
            else:
                a.append((k, v))

        formq_data = [dict() for _ in range(max_l)]
        for e in a:
            if len(e) == 1:
                k, v = e[0]
                for d in formq_data:
                    d[k] = v
            else:
                assert len(e) == max_l
                for d, ee in zip(formq_data, e):
                    k, v = ee
                    d[k] = v

        for form1_data in formq_data:
            forms = DeliveryOrderForm(form1_data)
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
                # messages.success(request, "Delivery order created successfully")
                # create_log(request, deliveryorder)
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

@login_required(login_url="/login")
def updateDO(request, pk):
    action = 'update'
    deliveryorder = DeliveryOrder.objects.get(id=pk)
    previous_do = deliveryorder.do_quantity
    form = DeliveryOrderForm(instance=deliveryorder)

    if request.method == 'POST':
        form = DeliveryOrderForm(request.POST, instance=deliveryorder)
        if form.is_valid():
            order = form.cleaned_data['order']
            do_quantity = form.cleaned_data['do_quantity']

            o = Order.objects.get(id=order.id)
            o.quantity -= do_quantity  # deduct quantity
            o.save()
            do = form.save()
            create_log(request, do, object_repr=do.do_quantity,
                       change_message=f"do_quantity {previous_do} to {do.do_quantity}")
            return redirect('do-list')

    context = {'action': action, 'form': form}
    return render(request, 'store/update_do.html', context)


def deleteDO(request, pk):
    deliveryorder = DeliveryOrder.objects.get(id=pk)
    if request.method == 'POST':
        deliveryorder_id = deliveryorder.order
        deliveryorder.delete()
        return redirect('do-list')

    return render(request, 'store/delete_do.html', {'item': deliveryorder})


@login_required(login_url='login')
def create_deliveryins(request):
    from django import forms
    form = DeliveryInsForm()

    if request.method == 'POST':
        forms = DeliveryInsForm(request.POST)
        if forms.is_valid():
            variant = forms.cleaned_data['variant']
            product = forms.cleaned_data['product']
            usage = forms.cleaned_data['usage']
            part = forms.cleaned_data['part']
            supplier = forms.cleaned_data['supplier']
            dimension = forms.cleaned_data['dimension']
            box = forms.cleaned_data['box']
            remarks = forms.cleaned_data['remarks']

            q = Part.objects.get(id=part.id)

            deliveryins = DeliveryIns.objects.create(
                variant=variant,
                usage=usage,
                product=product,
                part=part,
                supplier=supplier,
                dimension=dimension,
                box=box,
                remarks=remarks,
            )

            q.quan -= box  # deduct quantity
            q.save()
            # create_log(request, deliveryins)
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
        elif self.request.GET.get('product'):
            queryset = queryset.filter(product_id=self.request.GET.get('product'))
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
    previous_dins = deliveryins.box
    form = DeliveryInsForm(instance=deliveryins)

    if request.method == 'POST':
        form = DeliveryInsForm(request.POST, instance=deliveryins)
        if form.is_valid():
            part = form.cleaned_data['part']
            box = form.cleaned_data['box']

            q = Part.objects.get(id=part.id)
            q.quan -= box
            q.save()
            din = form.save()
            create_log(request, din, object_repr=din.box,
                       change_message=f"QTY {previous_dins} to {din.box} in Delivery Instructions")
            return redirect('dins-list')

    context = {'action': action, 'form': form}
    return render(request, 'store/update_dins.html', context)


def deleteDI(request, pk):
    deliveryins = DeliveryIns.objects.get(id=pk)
    if request.method == 'POST':
        deliveryins_id = deliveryins.part
        deliveryins.delete()
        return redirect('dins-list')

    return render(request, 'store/delete_dins.html', {'item': deliveryins})

@login_required(login_url='/login')
def logs(request):
    my_logs = LogEntry.objects.all()
    return render(request, 'store/logs.html', {'logs': my_logs})
