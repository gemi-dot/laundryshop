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
        name = self.cleaned_data['name']
        return name.strip().title()
 
class LaundryItemForm(forms.ModelForm):
    class Meta:
        model = LaundryItem
        fields = ['service', 'quantity']
        widgets = {
            'service': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        }



