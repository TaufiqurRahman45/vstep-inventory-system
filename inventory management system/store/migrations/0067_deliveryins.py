# Generated by Django 3.0.8 on 2021-07-01 06:24

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0066_delete_deliveryins'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryIns',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dimension', models.CharField(max_length=30)),
                ('box', models.PositiveIntegerField(default=0)),
                ('variant', models.CharField(choices=[('STD', 'STD'), ('EXEC', 'EXEC'), ('PREM', 'PREM'), ('SE', 'SE'), ('ALL', 'ALL'), ('PREM/FLAG', 'PREM/FLAG'), ('FLAG', 'FLAG'), ('STD/EXEC', 'STD/EXEC'), ('EXEC/PREM', 'EXEC/PREM')], max_length=20)),
                ('usage', models.PositiveIntegerField(default=0)),
                ('remarks', models.CharField(blank=True, max_length=500)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('part', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Part')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Product')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Supplier')),
            ],
        ),
    ]
