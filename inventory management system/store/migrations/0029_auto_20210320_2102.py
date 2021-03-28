# Generated by Django 3.0.8 on 2021-03-20 13:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0028_auto_20210320_1921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='is_ppc',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='order',
            name='new_stock',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
    ]
