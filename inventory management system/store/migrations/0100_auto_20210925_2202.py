# Generated by Django 3.0.8 on 2021-09-25 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0099_auto_20210925_2201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliveryins',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]