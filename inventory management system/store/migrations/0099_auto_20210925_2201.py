# Generated by Django 3.0.8 on 2021-09-25 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0098_auto_20210806_1417'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliveryins',
            name='created_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]