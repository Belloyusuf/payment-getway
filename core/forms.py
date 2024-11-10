from django import forms
from . models import Payment

class PaymentForm(forms.Form):
    class Meta:
        model = Payment
        fields = ("amount", "email")

