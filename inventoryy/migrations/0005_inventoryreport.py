# Generated by Django 5.0 on 2024-10-13 14:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventoryy', '0004_delete_inventoryreport'),
    ]

    operations = [
        migrations.CreateModel(
            name='InventoryReport',
            fields=[
                ('report_id', models.AutoField(primary_key=True, serialize=False)),
                ('report_date', models.DateTimeField(auto_now_add=True)),
                ('total_value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('generated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventoryy.manager')),
            ],
        ),
    ]
