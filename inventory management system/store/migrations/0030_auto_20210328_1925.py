# Generated by Django 3.0.8 on 2021-03-28 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0029_auto_20210320_2102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='new_stock',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]
