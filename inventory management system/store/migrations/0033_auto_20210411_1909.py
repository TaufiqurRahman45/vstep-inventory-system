# Generated by Django 3.0.8 on 2021-04-11 11:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0032_purchaseorder'),
    ]

    operations = [
        migrations.RenameField(
            model_name='purchaseorder',
            old_name='part',
            new_name='partno',
        ),
    ]