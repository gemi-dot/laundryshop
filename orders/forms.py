from django import forms
from .models import Customer, LaundryItem


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'address', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_name(self):
        # Automatically capitalize the name input
        name = self.cleaned_data['name']
        return name.strip().title()
 

class LaundryItemForm(forms.ModelForm):
    class Meta:
        model = LaundryItem
        fields = ['customer', 'service', 'quantity']

    SERVICE_CHOICES = [
        ('Wash Only', 'Wash Only'),
        ('Wash and Dry', 'Wash and Dry'),
        ('Wash, Dry and Fold', 'Wash, Dry and Fold'),
        ('Ironing', 'Ironing'),
    ]

    service = forms.ChoiceField(choices=SERVICE_CHOICES)
    quantity = forms.IntegerField(min_value=1)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically populate the customer queryset
        self.fields['customer'].queryset = Customer.objects.all()  

