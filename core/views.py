from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from . import forms

def initiate_payment(request):
    if request.method == "POST":
        payment_form = forms.PaymentForm(request.POST)
        if payment_form.is_valid():
            payment = payment_form.save()
            return render(request, 'make_payment.html', {
                'payment': payment,
                'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY
            })
    else:
        payment_form = forms.PaymentForm()
    
    return render(request, 'initiate_payment.html', {'payment_form': payment_form})

from .models import Payment

def verify_payment(request, ref:str):
    payment = get_object_or_404(Payment, ref=ref)
    verified = payment.verify_payment()
    return redirect('initiate-payment')
