# Generated by Django 3.0.8 on 2021-03-17 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0017_remove_order_drop'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='style',
            field=models.CharField(default='N/A', max_length=50),
        ),
    ]