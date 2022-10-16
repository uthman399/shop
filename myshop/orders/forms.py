from django import forms
from .models import Order
from django.forms import TextInput

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'phone_number', 'postal_code', 'city']
        widgets = {
            "first_name": TextInput(
                attrs={
                    "placeholder": "Enter your first name"
                }
            ),
            "last_name": TextInput(
                attrs={
                    "placeholder": "Enter your last name"
                }
            ),
            "email": TextInput(
                attrs={
                    "placeholder": "e.g. jason@example.com"
                }
            ),
            "address": TextInput(
                attrs={
                    "placeholder": "Enter your delivery address"
                }
            ),
            "postal_code": TextInput(
                attrs={
                    "placeholder": "e.g. 70098"
                }
            ),
            "phone_number": TextInput(
                attrs={
                    "placeholder": "e.g. 08012121212"
                }
            )
        }