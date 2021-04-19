# Generated by Django 3.0.8 on 2021-04-11 10:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0031_part'),
    ]

    operations = [
        migrations.CreateModel(
            name='PurchaseOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('terms', models.CharField(choices=[('30', '30'), ('60', '60'), ('90', '90')], max_length=10)),
                ('remarks', models.CharField(choices=[('follow di', 'Follow DI'), ('follow agent', 'Follow Agent')], max_length=20)),
                ('po_quantity', models.PositiveIntegerField(default=0)),
                ('amount', models.PositiveIntegerField(default=0)),
                ('created_date', models.DateField(auto_now_add=True)),
                ('part', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Part')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Product')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Supplier')),
            ],
        ),
    ]