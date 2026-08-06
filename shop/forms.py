from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    promo_code = forms.CharField(
        max_length=50,
        required=False,
        label='Промокод',
        widget=forms.TextInput(attrs={'placeholder': 'Введите промокод'})
    )

    class Meta:
        model = Order
        fields = ['full_name', 'address', 'phone', 'email', 'payment_method', 
                  'card_number', 'card_expiry', 'installment_months']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Иванов Иван Иванович', 'style': 'width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 8px; box-sizing: border-box;'}),
            'address': forms.Textarea(attrs={'placeholder': 'г. Ташкент, ул. Примерная, д. 1', 'rows': 3, 'style': 'width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 8px; box-sizing: border-box;'}),
            'phone': forms.TextInput(attrs={'placeholder': '+998 90 123 45 67', 'style': 'width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 8px; box-sizing: border-box;'}),
            'email': forms.EmailInput(attrs={'placeholder': 'ivan@example.com', 'style': 'width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 8px; box-sizing: border-box;'}),
            'payment_method': forms.RadioSelect(),
            'card_number': forms.TextInput(attrs={'placeholder': '1234 5678 9012 3456', 'maxlength': '19', 'style': 'width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 8px; box-sizing: border-box;'}),
            'card_expiry': forms.TextInput(attrs={'placeholder': 'MM/YY', 'maxlength': '5', 'style': 'width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 8px; box-sizing: border-box;'}),
            'installment_months': forms.Select(),
        }