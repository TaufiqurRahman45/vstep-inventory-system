# Generated by Django 3.0.8 on 2021-06-04 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0059_order_new_stock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='new_stock',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='part',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
    ]