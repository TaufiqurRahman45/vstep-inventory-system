# Generated by Django 3.0.8 on 2021-07-12 08:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0091_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='created_date',
        ),
    ]
