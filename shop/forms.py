from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'address', 'phone', 'email']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Иванов Иван Иванович'}),
            'address': forms.Textarea(attrs={'placeholder': 'г. Ташкент, ул. Примерная, д. 1', 'rows': 3}),
            'phone': forms.TextInput(attrs={'placeholder': '+998 90 123 45 67'}),
            'email': forms.EmailInput(attrs={'placeholder': 'ivan@example.com'}),
        }