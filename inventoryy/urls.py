from django.urls import path
from . import views

urlpatterns = [
    path('', views.inventoryy, name='inventoryy'),
    path('login/', views.login, name='login'),  # Login page
    path('signup/', views.signup, name='signup'),  # Sign up page



    path('staff_homepage/<str:staffID>', views.staff_homepage, name='staff_homepage'),  # Staff home page
    path('record_items/<str:staff_id>/', views.record_items, name='record_items'),
    path('save_transaction/', views.save_transaction, name='save_transaction'),
    path('transaction_history/<str:staff_id>/', views.transaction_history, name='transaction_history'),

    path('purchase_items/<str:staff_id>', views.purchase_items, name='purchase_items'),
    path('inventory/<str:staff_id>', views.inventory, name='inventory'),  # Inventory page

    # MANAGER

    path('manager_homepage/<str:managerid>/', views.manager_homepage, name='manager_homepage'), 
    path('generate_report/<str:manager_id>/', views.generate_report, name='generate_report'),

    path('staff_details/<str:manager_id>/', views.staff_details, name='staff_details'),
    path('add_staff/<str:manager_id>/', views.add_staff, name='add_staff'),

    path('update_staff/<str:staff_id>/<str:manager_id>/', views.update_staff, name='update_staff'),
    path('delete_staff/<str:staff_id>/<str:manager_id>/', views.delete_staff, name='delete_staff'),


    # Other URL patterns...



    path('item_details/<str:manager_id>/', views.item_details, name='item_details'),

    path('update_item/<str:item_id>/<str:manager_id>/', views.update_item, name='update_item'),
    path('delete_item/<str:item_id>/<str:manager_id>/', views.delete_item, name='delete_item'),


    path('supplier_details/<str:manager_id>/', views.supplier_details, name='supplier_details'),
    path('update_supplier/<str:supplier_id>/<str:manager_id>/', views.update_supplier, name='update_supplier'),
    path('delete_supplier/<str:supplier_id>/<str:manager_id>/', views.delete_supplier, name='delete_supplier'),
]