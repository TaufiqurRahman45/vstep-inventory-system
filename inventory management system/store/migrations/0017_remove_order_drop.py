# Generated by Django 3.0.8 on 2021-03-17 10:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0016_auto_20210317_1822'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='drop',
        ),
    ]
