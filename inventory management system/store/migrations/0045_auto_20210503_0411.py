# Generated by Django 3.0.8 on 2021-05-02 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0044_auto_20210503_0355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliveryins',
            name='dimension',
            field=models.CharField(max_length=30),
        ),
    ]