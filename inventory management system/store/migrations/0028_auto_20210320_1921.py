# Generated by Django 3.0.8 on 2021-03-20 11:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0027_supplier_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='delivery',
            name='order',
        ),
        migrations.DeleteModel(
            name='Drop',
        ),
        migrations.DeleteModel(
            name='Season',
        ),
        migrations.DeleteModel(
            name='Delivery',
        ),
    ]
