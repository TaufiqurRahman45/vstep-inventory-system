# Generated by Django 3.0.8 on 2021-03-16 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_delete_purchaseorder'),
    ]

    operations = [
        migrations.CreateModel(
            name='Purchaseorder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, unique=True)),
            ],
        ),
    ]
