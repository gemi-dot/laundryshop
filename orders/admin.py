from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Customer, LaundryItem

admin.site.register(Customer)
admin.site.register(LaundryItem)
