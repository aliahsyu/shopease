# Generated by Django 5.0 on 2024-10-12 08:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('item_id', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('item_name', models.CharField(max_length=255)),
                ('category', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('stock_quantity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('manager_id', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('manager_name', models.CharField(max_length=255)),
                ('manager_password', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('staff_id', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('staff_name', models.CharField(max_length=255)),
                ('staff_password', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('supplier_id', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('supplier_name', models.CharField(max_length=255)),
                ('supplier_phone_number', models.CharField(max_length=20)),
                ('supplier_address', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('transaction_id', models.AutoField(primary_key=True, serialize=False)),
                ('transaction_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('transaction_date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventoryy.staff')),
            ],
        ),
        migrations.CreateModel(
            name='TransactionItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('item_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventoryy.item')),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventoryy.transaction')),
            ],
        ),
    ]
