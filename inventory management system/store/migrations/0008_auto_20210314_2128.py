# Generated by Django 3.0.8 on 2021-03-14 13:28

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    atomic = False
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0007_auto_20210314_1915'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Buyer',
            new_name='Purchaseorder',
        ),
        migrations.RemoveField(
            model_name='order',
            name='buyer',
        ),
    ]
