from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['address', 'phone_number']

    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True,
        label="Номер телефона"
    )

class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['order_status']