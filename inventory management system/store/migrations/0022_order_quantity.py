# Generated by Django 3.0.8 on 2021-03-17 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0021_order_standard'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='quantity',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
