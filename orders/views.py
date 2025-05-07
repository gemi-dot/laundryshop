from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer, LaundryItem
from .forms import CustomerForm, LaundryItemForm

from django.db.models import Q
from django.core.paginator import Paginator

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
    search_query = request.GET.get('q', '')  # Get search query from URL parameters
    customers = Customer.objects.all()

    # Apply search filter if there's a search query
    if search_query:
        customers = customers.filter(
            Q(name__icontains=search_query) | 
            Q(address__icontains=search_query) | 
            Q(phone__icontains=search_query)
        )

    # Pagination logic: 10 customers per page
    paginator = Paginator(customers, 10)
    page_number = request.GET.get('page')  # Get page number from URL parameters
    page_obj = paginator.get_page(page_number)  # Get customers for the current page

    # Render the customer list template
    return render(request, 'orders/customer_list.html', {
        'page_obj': page_obj,  # Pass paginated customers to the template
        'search_query': search_query  # Pass the search query to maintain it in the form
    })
