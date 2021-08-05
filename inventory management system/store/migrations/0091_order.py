# Generated by Django 3.0.8 on 2021-07-12 08:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import store.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0090_auto_20210712_1620'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('po_id', models.CharField(default=store.models.random_string, max_length=4)),
                ('terms', models.CharField(choices=[('30', '30'), ('60', '60'), ('90', '90')], max_length=10)),
                ('remarks', models.CharField(choices=[('follow di', 'Follow DI'), ('follow agent', 'Follow Agent')], max_length=20)),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('created_date', models.DateField(auto_now_add=True)),
                ('po_date', models.DateField()),
                ('new_stock', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('is_ppc', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('part', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Part')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Product')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Supplier')),
            ],
        ),
    ]