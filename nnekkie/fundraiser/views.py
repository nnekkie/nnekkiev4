from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse
from .forms import PaymentForm
from .models import Payment
from django.conf import settings
from django.contrib import messages
# Create your views here.

def verify_payment(request : HttpRequest, ref :str) -> HttpResponse:
    payment = get_object_or_404(Payment, ref=ref)
    verified = payment.verify_payment()
    if verified:
        messages.success(request, 'Verification successful')
    else:
        messages.error(request, 'Verification failed')
    return redirect('fundraiser:initiate-payment')

def initiate_payment(request : HttpRequest) -> HttpResponse:
    payment_form = PaymentForm()
    if request.method == 'POST':
        payment_form =  PaymentForm(request.POST)
        if payment_form.is_valid():
            payment = payment_form.save()  # Assuming user is available in the request
         

            return render(request,'fund/make.html', {'payment':payment,'paystack_public_key':settings.PAYSTACK_PUBLIC_KEY})
        
        else :
            payment_form =PaymentForm()
    return render(request, 'fund/index.html', {'payment_form':payment_form})