# Generated by Django 3.0.8 on 2021-08-05 22:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0094_auto_20210805_2247'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='part',
            name='usage',
        ),
        migrations.RemoveField(
            model_name='part',
            name='variant',
        ),
    ]