# Generated by Django 3.0.8 on 2021-07-12 07:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0086_auto_20210712_1549'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='is_ppc',
        ),
        migrations.RemoveField(
            model_name='order',
            name='part',
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
