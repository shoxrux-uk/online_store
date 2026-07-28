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
            'full_name': forms.TextInput(attrs={'placeholder': 'Иванов Иван Иванович'}),
            'address': forms.Textarea(attrs={'placeholder': 'г. Ташкент, ул. Примерная, д. 1', 'rows': 3}),
            'phone': forms.TextInput(attrs={'placeholder': '+998 90 123 45 67'}),
            'email': forms.EmailInput(attrs={'placeholder': 'ivan@example.com'}),
            'payment_method': forms.RadioSelect(),
            'card_number': forms.TextInput(attrs={'placeholder': '1234 5678 9012 3456', 'maxlength': '19'}),
            'card_expiry': forms.TextInput(attrs={'placeholder': 'MM/YY', 'maxlength': '5'}),
            'installment_months': forms.Select(),
        }
        labels = {
            'card_number': 'Номер карты',
            'card_expiry': 'Срок действия (MM/YY)',
            'installment_months': 'Срок рассрочки',
        }