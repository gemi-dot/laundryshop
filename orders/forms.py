from django import forms
from .models import Customer, LaundryItem

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        #fields = ['name']

        fields = ['name', 'address', 'phone']

    def clean_name(self):
        name = self.cleaned_data['name']
        return name.strip().title()  # Converts to e.g., 'Badot' or 'Gemi'   

class LaundryItemForm(forms.ModelForm):
    class Meta:
        model = LaundryItem
        fields = ['service', 'quantity']


