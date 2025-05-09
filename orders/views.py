from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer, LaundryItem
from .forms import CustomerForm, LaundryItemForm

from django.urls import reverse

from django.db.models import Q
from django.core.paginator import Paginator


def main_menu(request):
    return render(request, 'orders/main_menu.html')



def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_list')  # Redirect to customer list after creation
    else:
        form = CustomerForm()

    return render(request, 'orders/customer_create.html', {'form': form})

# Edit customer details
def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            print("Form is valid and saved")
            return redirect('customer_detail', pk=customer.pk)  # Redirect to the customer detail page
    else:
        form = CustomerForm(instance=customer)
 
    return render(request, 'orders/customer_edit.html', {'form': form, 'customer': customer})

# Delete customer
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('customer_list')  # Redirect back to the customer list page
    return render(request, 'orders/customer_confirm_delete.html', {'customer': customer})

# Add order
def add_order(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            request.session['customer_id'] = customer.id
            return redirect('add_items')
    else:
        form = CustomerForm()
    return render(request, 'orders/add_order.html', {'form': form})

# Add items to the order
def add_items(request):
    customer_id = request.session.get('customer_id')
    customer = get_object_or_404(Customer, id=customer_id)

    if request.method == 'POST':
        form = LaundryItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.customer = customer
            item.save()
            return redirect('add_items')
    else:
        form = LaundryItemForm()

    items = LaundryItem.objects.filter(customer=customer)
    total = customer.total_spent()

    return render(request, 'orders/add_items.html', {
        'form': form,
        'customer': customer,
        'items': items,
        'total': total
    })

# Customer details
def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    return render(request, 'orders/customer_detail.html', {'customer': customer})

# Customer history
def customer_history(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    items = LaundryItem.objects.filter(customer=customer)
    total = customer.total_spent()

    return render(request, 'orders/customer_history.html', {
        'customer': customer,
        'items': items,
        'total': total
    })

# List customers with search and pagination

def customer_list(request):
    query = request.GET.get('q', '')
    customers = Customer.objects.exclude(pk=1)  # 👈 exclude customer with pk=1

    if query:
        customers = customers.filter(name__icontains=query)

    paginator = Paginator(customers, 10)  # Adjust number per page as needed
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'orders/customer_list.html', {'page_obj': page_obj})




def laundry_item_list(request):
    laundry_items = LaundryItem.objects.select_related('customer').order_by('-date_added')
    return render(request, 'orders/laundry_item_list.html', {'laundry_items': laundry_items})


def laundry_item_create(request):
    if request.method == 'POST':
        form = LaundryItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('laundry_item_list')
    else:
        form = LaundryItemForm()
    return render(request, 'orders/laundry_item_form.html', {'form': form})


def laundry_item_edit(request, pk):
    laundry_item = get_object_or_404(LaundryItem, pk=pk)
    
    if request.method == 'POST':
        customer_id = request.POST.get('customer')
        service = request.POST.get('service')
        quantity = request.POST.get('quantity')

        # Update the laundry item with the new data
        laundry_item.customer = Customer.objects.get(id=customer_id)
        laundry_item.service = service
        laundry_item.quantity = quantity
        laundry_item.save()

        return redirect('laundry_item_list')  # Redirect back to the laundry item list
    
    customers = Customer.objects.all()  # Get all customers for the dropdown
    return render(request, 'orders/laundry_item_edit.html', {'laundry_item': laundry_item, 'customers': customers})


def laundry_item_delete(request, pk):
    item = get_object_or_404(LaundryItem, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('laundry_item_list')
    #return render(request, 'laundry/laundry_item_confirm_delete.html', {'item': item})
    
    return render(request, 'orders/laundry_item_delete.html', {'item': item})




def add_laundry_item(request):
    if request.method == 'POST':
        form = LaundryItemForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new laundry item to the database
            return redirect('laundry_item_list')  # Redirect to the laundry item list page
    else:
        form = LaundryItemForm()

    return render(request, 'laundry/laundry_item_add.html', {'form': form})


