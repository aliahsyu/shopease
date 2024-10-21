from django.db import models

# Create your models here.

class Staff(models.Model):
    staff_id = models.CharField(primary_key = True, max_length = 15)
    staff_name = models.CharField(max_length = 255)
    staff_password = models.CharField(max_length = 20)

class Manager(models.Model):
    manager_id =  models.CharField(primary_key = True, max_length = 15)
    manager_name = models.CharField(max_length = 255)
    manager_password = models.CharField(max_length = 20)



class Supplier(models.Model):
    supplier_id = models.CharField(primary_key = True, max_length = 15)
    supplier_name = models.CharField(max_length = 255)
    supplier_phone_number = models.CharField(max_length = 20)
    supplier_address = models.CharField(max_length = 255)

class Item(models.Model):
    item_id = models.CharField(primary_key = True, max_length = 15)
    item_name = models.CharField(max_length = 255)
    category = models.CharField(max_length = 255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField()
      
class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Staff, on_delete=models.CASCADE)
    transaction_price = models.DecimalField(max_digits=10, decimal_places=2)  # Total transaction price
    transaction_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50) 

class TransactionItem(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    item_price = models.DecimalField(max_digits=10, decimal_places=2)

class InventoryReport(models.Model):
    report_id = models.AutoField(primary_key=True)  # Unique report ID
    report_date = models.DateTimeField(auto_now_add=True)  # Date when the report is generated
    total_value = models.DecimalField(max_digits=10, decimal_places=2)  # Total value of inventory
    generated_by = models.ForeignKey(Manager, on_delete=models.CASCADE)  # The manager who generated the report

    def __str__(self):
        return f'Report ID: {self.report_id}, Date: {self.report_date}, Transaction Price: {self.transaction.transaction_price}'