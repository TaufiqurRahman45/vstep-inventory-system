# Generated by Django 3.0.8 on 2021-08-05 22:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0093_deliveryorder'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='po_date',
            new_name='created_date',
        ),
    ]