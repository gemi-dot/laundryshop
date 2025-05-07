from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer, LaundryItem
from .forms import CustomerForm, LaundryItemForm

from django.db.models import Q
from django.core.paginator import Paginator



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

