from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_menu, name='main_menu'),

    # Customer paths
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/create/', views.customer_create, name='customer_create'),
    path('customers/<int:pk>/', views.customer_detail, name='customer_detail'),
    path('customers/<int:pk>/edit/', views.customer_edit, name='customer_edit'),
    path('customers/<int:pk>/delete/', views.customer_delete, name='customer_delete'),
    path('customers/<int:customer_id>/history/', views.customer_history, name='customer_history'),

    # Laundry item paths
    path('laundry-items/', views.laundry_item_list, name='laundry_item_list'),
    path('laundry-items/add/', views.laundry_item_create, name='laundry_item_add'),
    path('laundry-items/<int:pk>/edit/', views.laundry_item_edit, name='laundry_item_edit'),
    path('laundry-items/<int:pk>/delete/', views.laundry_item_delete, name='laundry_item_delete'),

    # Order workflow paths
    path('add-order/', views.add_order, name='add_order'),
    path('add-items/', views.add_items, name='add_items'),
]
