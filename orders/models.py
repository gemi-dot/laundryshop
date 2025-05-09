from django.db import models
from django.utils import timezone

# Customer Model
class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)  # Allow null values
    created_at = models.DateTimeField(auto_now_add=True)

    def total_spent(self):
        return sum(item.total_price() for item in self.laundryitem_set.all())

    def __str__(self):
        return self.name


# LaundryItem Model
class LaundryItem(models.Model):
    SERVICE_CHOICES = [
        ("Wash Only", 50),
        ("Wash and Dry", 80),
        ("Wash, Dry and Fold", 100),
        ("Ironing", 30),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    service = models.CharField(max_length=30, choices=[(s[0], s[0]) for s in SERVICE_CHOICES])
    quantity = models.PositiveIntegerField()
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.service} ({self.quantity})"
    
    def unit_price(self):
        return dict(self.SERVICE_CHOICES)[self.service]

    def total_price(self):
        return self.unit_price() * self.quantity
