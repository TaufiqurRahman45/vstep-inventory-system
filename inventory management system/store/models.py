from django.db import models

from django.utils import timezone

from users.models import User

import datetime

import random

class Supplier(models.Model):
    name = models.CharField(max_length=120, unique=True)
    address = models.CharField(max_length=220)
    address2 = models.CharField(max_length=220, default="No Address 2")
    address3 = models.CharField(max_length=220, default="No Address 3")
    postcode = models.CharField(max_length=10, default="No Postcode")
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=220)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=120, unique=True)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

class Part(models.Model):
    partno = models.CharField(max_length=50)
    partname = models.CharField(max_length=50)
    stylepack = models.CharField(max_length=50, blank= True)
    standardpack = models.PositiveIntegerField(default= 0)
    quan = models.PositiveIntegerField(default= 0)
    limit = models.PositiveIntegerField(default= 0)
    unit = models.PositiveIntegerField(default= 0)
    price = models.DecimalField(default= 0,max_digits=5, decimal_places=2)
    tax = models.PositiveIntegerField(default= 0)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.partname


def random_string():

    return str(random.randint(1000, 9999))

class Order(models.Model):
    terms = (
        ('30', '30'),
        ('60', '60'),
        ('90', '90'),
    )

    remarks = (
        ('follow di', 'Follow DI'),
        ('follow agent', 'Follow Agent'),
    )
    po_id = models.CharField(max_length=4, default = random_string)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    terms = models.CharField(max_length=10, choices=terms)
    remarks = models.CharField(max_length=20, choices=remarks)
    quantity = models.PositiveIntegerField(default= 0)
    created_date = models.DateField(auto_now_add=True)
    is_ppc = models.ForeignKey(User, on_delete=models.CASCADE, null=True,)
    new_stock = models.PositiveIntegerField(default=0, blank=True, null=True)

    @property
    def amount(self):
        return self.part.price * self.quantity

    def __str__(self):
        return self.part.partname



class DeliveryOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    do_quantity = models.PositiveIntegerField(default= 0)
    created_date = models.DateField(auto_now_add=True)

class EventManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(
            created_date__gte=timezone.now()-timezone.timedelta(days=1)
        )

def di_id():

    return str(random.randint(1000, 9999))

class DeliveryIns(models.Model):
    variant = (
        ('STD', 'STD'),
        ('EXEC', 'EXEC'),
        ('PREM', 'PREM'),
        ('SE', 'SE'),
        ('ALL', 'ALL'),
        ('PREM/FLAG', 'PREM/FLAG'),
        ('FLAG', 'FLAG'),
        ('STD/EXEC', 'STD/EXEC'),
        ('EXEC/PREM', 'EXEC/PREM'),
    )
    di_id = models.CharField(max_length=4, default = di_id)
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    dimension =  models.CharField(max_length=30)
    box = models.PositiveIntegerField(default= 0)  
    variant = models.CharField(max_length=20, choices=variant)
    usage = models.PositiveIntegerField(default= 0) 
    remarks = models.CharField(max_length=500, blank= True)
    created_date = models.DateTimeField(default=timezone.now)
    objects = EventManager()

   