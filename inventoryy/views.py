from django.shortcuts import render, redirect
from .models import Staff, Manager, Item, Supplier, Transaction, TransactionItem, InventoryReport
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.http import HttpResponse 
from django.views.decorators.csrf import csrf_exempt
import json

def inventoryy(request):
    return HttpResponse("Please use this http://127.0.0.1:8000/login/")



# def home(request):
#     return render(request, 'home.html') 

def check_low_stock():
    low_stock_items = Item.objects.filter(stock_quantity__lt=30)
    return low_stock_items




################################## LOGIN ##########################################
def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        user_id = request.POST.get("user_id")
        password = request.POST.get("password")
        role = request.POST.get("role")

        if not username or not user_id or not password or not role:
            # If any of the fields are missing
            message = {"message": "Please fill in all fields."}
            return render(request, 'login.html', message)

        if role == "staff":  # Staff login
            try:
                staff = Staff.objects.get(staff_id=user_id)
                if staff:
                    return redirect('staff_homepage', staffID=staff.staff_id)
                else:
                    message = {"message": "Invalid staff ID or password"}
                    return render(request, 'login.html', message)
            except Staff.DoesNotExist:
                message = {"message": "Invalid staff ID or password"}
                return render(request, 'login.html', message)

        elif role == "manager":  # Manager login
            try:
                manager = Manager.objects.get(manager_id=user_id)
                if manager:
                    return redirect('manager_homepage', managerid=manager.manager_id)
                else:
                    message = {"message": "Invalid manager ID or password"}
                    return render(request, 'login.html', message)
            except Manager.DoesNotExist:
                message = {"message": "Invalid manager ID or password"}
                return render(request, 'login.html', message)

        else:
            # Handle invalid role
            message = {"message": "Invalid role"}
            return render(request, 'login.html', message)
    else:
        return render(request, 'login.html')
##################################  ##########################################




################################## SIGNUP ##########################################
def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        user_id = request.POST["user_id"]
        password = request.POST["password"]
        role = request.POST["role"]

        # Determine the role and save the new user data
        if role == "staff":
            if Staff.objects.filter(staff_id=user_id).exists():
                message = {"message": "Staff ID already exists"}
                return render(request, 'signup.html', message)
            else:
                new_staff = Staff(staff_id=user_id, staff_name=username, staff_password=password)
                new_staff.save()
                return redirect('login')  # Redirect to login page after successful signup

        elif role == "manager":
            if Manager.objects.filter(manager_id=user_id).exists():
                message = {"message": "Manager ID already exists"}
                return render(request, 'signup.html', message)
            else:
                new_manager = Manager(manager_id=user_id, manager_name=username, manager_password=password)
                new_manager.save()
                return redirect('login')  # Redirect to login page after successful signup

        else:
            # Invalid role selected
            message = {"message": "Invalid role selected"}
            return render(request, 'signup.html', message)

    return render(request, 'signup.html')

##################################  ##########################################



################################## STAFF HOMEPAGE ##########################################
def staff_homepage(request,staffID):
    low_stock_items = Item.objects.filter(stock_quantity__lt=30)
    low_stock_info = [{'name': item.item_name, 'stock': item.stock_quantity} for item in low_stock_items]
    userID = {
        'low_stock_info': low_stock_info,
        "userId":staffID
        }
    return render(request, 'staff_homepage.html',userID)








def record_items(request, staff_id):
    items = Item.objects.all()  # Get all items from the database
    
    context = {
        'items': items,
        'staff_id': staff_id
    }
    return render(request, 'record_items.html', context)

@csrf_exempt
def save_transaction(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        staff_id = data.get('staff_id')
        items = data.get('items')
        total_price = data.get('total_price')
        payment_method = data.get('payment_method')  # Get the payment method from the request

        try:
            # Retrieve the staff object using staff_id
            staff = Staff.objects.get(staff_id=staff_id)

            # Create a single transaction record, including payment_method
            transaction = Transaction.objects.create(
                user=staff,
                transaction_price=total_price,
                payment_method=payment_method  # Save payment method here
            )

            # Loop through each item in the transaction and save item details
            for item_data in items:
                item_name = item_data['name']
                quantity = int(item_data['quantity'])
                price = float(item_data['price'])

                # Fetch the item from the database
                item = Item.objects.get(item_name=item_name)

                # Check if there is enough stock
                if item.stock_quantity < quantity:
                    return JsonResponse({'success': False, 'error': f'Not enough stock for {item_name}.'})

                # Deduct the stock from the item
                item.stock_quantity -= quantity
                item.save()

                # Save the item details to the transaction (per item in the single transaction)
                TransactionItem.objects.create(
                    transaction=transaction,
                    item=item,
                    quantity=quantity,
                    item_price=price
                )

            return JsonResponse({'success': True})

        except Staff.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Staff not found.'})
        except Item.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Item not found.'})
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method.'})


def transaction_history(request, staff_id):
    try:
        # Retrieve the staff member
        staff = Staff.objects.get(staff_id=staff_id)

        # Get all transactions for the staff member
        transactions = Transaction.objects.filter(user=staff).order_by('-transaction_date')

        # Prepare context data with transaction details
        context = {
            'staff': staff,
            'transactions': transactions,
            'staff_id': staff_id
        }

        return render(request, 'transaction_history.html', context)

    except Staff.DoesNotExist:
        return render(request, 'transaction_history.html', {'error': 'Staff not found.'})




def inventory(request, staff_id):
    items = Item.objects.all()  # Get all items from the database
    low_stock_items = Item.objects.filter(stock_quantity__lt=30)
    low_stock_info = [{'name': item.item_name, 'stock': item.stock_quantity} for item in low_stock_items]

    context = {
        'items': items,
        'low_stock_info': low_stock_info,
        'staff_id': staff_id
    }
    return render(request, 'inventory.html', context)








def purchase_items(request, staff_id):
    transaction = Transaction.objects.all()  # Get all staff from the database
    
    context = {
        'transaction': transaction,
        'staff_id': staff_id
    }
    return render(request, 'purchase_items.html', context)


# MANAGER

def manager_homepage(request, managerid):
    low_stock_items = Item.objects.filter(stock_quantity__lt=30)
    low_stock_info = [{'name': item.item_name, 'stock': item.stock_quantity} for item in low_stock_items]
    userID = {
        'low_stock_info': low_stock_info,
        "userId": managerid,  # Make sure this variable is defined correctly
    }
    return render(request, 'manager_homepage.html', userID)

#####################################################staff Details

# View to display staff details and handle delete
def staff_details(request, manager_id):
    staff_members = Staff.objects.all()  # Get all staff from the database
    low_stock_items = Item.objects.filter(stock_quantity__lt=30)
    low_stock_info = [{'name': item.item_name, 'stock': item.stock_quantity} for item in low_stock_items]
    if request.method == 'POST':
        staff_id = request.POST.get('staff_id')
        staff_name = request.POST.get('staff_name')
        staff_password = request.POST.get('staff_password')

        Staff.objects.create(staff_id=staff_id, staff_name=staff_name, staff_password=staff_password)    
        return redirect('staff_details', manager_id=manager_id)
    context = {
        'low_stock_info': low_stock_info,
        'staff_members': staff_members,
        'manager_id': manager_id
    }
    return render(request, 'staff_details.html', context)

# View to add a new staff member
def add_staff(request, manager_id):
    if request.method == 'POST':
        staff_id = request.POST.get('staff_id')
        staff_name = request.POST.get('staff_name')
        staff_password = request.POST.get('staff_password')

        # Create a new staff member instance
        new_staff = Staff(
            staff_id=staff_id,
            staff_name=staff_name,
            staff_password=staff_password
        )
        new_staff.save()

        return redirect('staff_details', manager_id=manager_id)

    context = {
        'manager_id': manager_id
    }
    return render(request, 'add_staff.html', context)


# View to update a staff member
def update_staff(request, staff_id, manager_id):
    staff = get_object_or_404(Staff, pk=staff_id)

    if request.method == 'POST':
        staff.staff_name = request.POST.get('staff_name')
        staff.staff_password = request.POST.get('staff_password')
        staff.save()

        return redirect('staff_details', manager_id=manager_id)

    context = {
        'staff': staff,
        'manager_id': manager_id
    }
    return render(request, 'update_staff.html', context)

# View to delete a staff member
def delete_staff(request, staff_id, manager_id):
    staff = get_object_or_404(Staff, pk=staff_id)
    staff.delete()

    return redirect('staff_details', manager_id=manager_id)







#######################################Item Details




def item_details(request, manager_id):
    items = Item.objects.all()  # Get all items from the database
    low_stock_items = []  # Create a list to hold items with low stock

    for item in items:
        if item.stock_quantity < 30:  # If stock is below 30, add to low_stock_items
            low_stock_items.append(item)
    
    if request.method == 'POST':
        # Get data from the form to add a new item
        item_id = request.POST.get('item_id')
        item_name = request.POST.get('item_name')
        category = request.POST.get('category')
        price = request.POST.get('price')
        stock_quantity = request.POST.get('stock_quantity')

        # Create a new item
        Item.objects.create(item_id=item_id, item_name=item_name, price=price, stock_quantity=stock_quantity, category=category)
        return redirect('item_details', manager_id=manager_id)

    context = {
        'items': items,
        'low_stock_items': low_stock_items,  # Add the list of low stock items to the context
        'manager_id': manager_id
    }
    return render(request, 'item_details.html', context)



# View to update an existing item
def update_item(request, item_id, manager_id):
    item = get_object_or_404(Item, pk=item_id)

    if request.method == 'POST':
        item.item_name = request.POST.get('item_name')
        item.price = request.POST.get('price')
        item.stock_quantity = request.POST.get('stock_quantity')
        item.save()

        return redirect('item_details', manager_id=manager_id)

    context = {
        'item': item,
        'manager_id': manager_id
    }
    return render(request, 'update_item.html', context)


# View to delete an item
def delete_item(request, item_id, manager_id):
    item = get_object_or_404(Item, pk=item_id)
    item.delete()

    return redirect('item_details', manager_id=manager_id)

################################################################






#############################################################Supplier details


# View to list suppliers and add new ones
def supplier_details(request, manager_id):
    suppliers = Supplier.objects.all()  # Get all suppliers from the database
    low_stock_items = Item.objects.filter(stock_quantity__lt=30)
    low_stock_info = [{'name': item.item_name, 'stock': item.stock_quantity} for item in low_stock_items]
    
    if request.method == 'POST':
        # Get data from the form to add a new supplier
        supplier_id = request.POST.get('supplier_id')
        supplier_name = request.POST.get('supplier_name')
        supplier_phone_number = request.POST.get('supplier_phone_number')
        supplier_address = request.POST.get('supplier_address')
        
        # Create new supplier
        Supplier.objects.create(
            supplier_id=supplier_id,
            supplier_name=supplier_name,
            supplier_phone_number=supplier_phone_number,
            supplier_address=supplier_address
        )
        return redirect('supplier_details', manager_id=manager_id)

    context = {
        'low_stock_info': low_stock_info,
        'suppliers': suppliers,
        'manager_id': manager_id
    }
    return render(request, 'supplier_details.html', context)


# View to update an existing supplier
def update_supplier(request, supplier_id, manager_id):
    supplier = get_object_or_404(Supplier, pk=supplier_id)

    if request.method == 'POST':
        supplier.supplier_name = request.POST.get('supplier_name')
        supplier.supplier_phone_number = request.POST.get('supplier_phone_number')
        supplier.supplier_address = request.POST.get('supplier_address')
        supplier.save()

        return redirect('supplier_details', manager_id=manager_id)

    context = {
        'supplier': supplier,
        'manager_id': manager_id
    }
    return render(request, 'update_supplier.html', context)


# View to delete a supplier
def delete_supplier(request, supplier_id, manager_id):
    supplier = get_object_or_404(Supplier, pk=supplier_id)
    supplier.delete()

    return redirect('supplier_details', manager_id=manager_id)

###########################################################################

from django.db.models.functions import TruncDate
from django.utils import timezone
from django.db.models import Sum
from datetime import timedelta
from django.db.models import Count, Q

def generate_report(request, manager_id):
    # Calculate the start and end of the week (Sunday to Saturday)
    today = timezone.now()
    start_of_week = today - timedelta(days=today.weekday() + 1)  # Last Sunday
    end_of_week = start_of_week + timedelta(days=7)  # Saturday of that week

    # Retrieve all transaction items for the week
    transaction_items = TransactionItem.objects.filter(
        transaction__transaction_date__range=[start_of_week, end_of_week]
    )

    # Calculate total sales for the week
    total_sales = transaction_items.aggregate(total_value=Sum('item_price'))['total_value'] or 0

    # Create and save the inventory report
    report = InventoryReport.objects.create(
        total_value=total_sales,
        generated_by_id=manager_id  # Assuming manager_id is the ID of the logged-in manager
    )

    # Group by date for detailed daily sales
    daily_sales = (
        transaction_items
        .values(date=TruncDate('transaction__transaction_date'))
        .annotate(total_sales=Sum('item_price'))
        .order_by('-date')
    )

    # Calculate product sales
    product_sales = (
        TransactionItem.objects
        .values('item__item_name')
        .annotate(total_quantity=Sum('quantity'), total_value=Sum('item_price'))
        .order_by('-total_value')
    )

    # Fast-selling products: Total sales above 35
    fast_selling_products = product_sales.filter(total_quantity__gt=35)

    # Slow-selling products: Total sales below 10
    slow_selling_products = product_sales.filter(total_quantity__lt=10)

    context = {
        'user_id': manager_id,
        'transaction_items': transaction_items,
        'daily_sales': daily_sales,
        'report': report,  # Pass the report object to the template
        'fast_selling_products': fast_selling_products,
        'slow_selling_products': slow_selling_products
    }

    return render(request, 'generate_report.html', context)
