from django.db import models

from users.models import User

class Supplier(models.Model):
    name = models.CharField(max_length=120, unique=True)
    address = models.CharField(max_length=220)
    email = models.CharField(max_length=220)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=120, unique=True)
    sortno = models.PositiveIntegerField()
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    partno = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    style = models.CharField(max_length=50, blank= True)
    standard = models.PositiveIntegerField(default= 0)
    quantity = models.PositiveIntegerField(default= 0)
    limit = models.PositiveIntegerField(default= 0)
    created_date = models.DateField(auto_now_add=True)
    is_ppc = models.ForeignKey(User, on_delete=models.CASCADE, null=True,)
    new_stock = models.PositiveIntegerField(default= 0, blank=True)

    def __str__(self):
        return self.product.name