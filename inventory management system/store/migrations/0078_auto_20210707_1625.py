# Generated by Django 3.0.8 on 2021-07-07 08:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0077_part'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='is_ppc',
        ),
        migrations.RemoveField(
            model_name='order',
            name='product',
        ),
        migrations.RemoveField(
            model_name='order',
            name='supplier',
        ),
        migrations.DeleteModel(
            name='DeliveryOrder',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
    ]
