from django.shortcuts import render, get_object_or_404
from django.http import *
from product.models import *
from .models import *
import random
from django.urls import reverse
import stripe
from facebook_prj.env import config
STRIPE_SECRET_KEY = config("STRIPE_SECRET_KEY", default=None)
stripe.api_key = STRIPE_SECRET_KEY
# Create your views here.

base_endpoint = "http://127.0.0.1:8000"
def purchase_start_view(request):
    if not request.method == "POST":
        return HttpResponseBadRequest()
    if not request.user.is_authenticated:
        return HttpResponseBadRequest()
    handle = request.POST.get("handle")
    obj = Product.objects.get(handle=handle)
    stripe_price_id = obj.stripe_price_id
    if stripe_price_id is None:
        return HttpResponseBadRequest()
    purchase = Purchase.objects.create(user=request.user, product=obj)
    request.session['purchase_id'] = purchase.id
    success_path = reverse("purchases:success")
    if not success_path.startswith("/"):
        success_path = f"/{success_path}"
    cancel_path = reverse("purchases:stopped")
    success_url = f"{base_endpoint}{success_path}"
    cancel_url = f"{base_endpoint}{cancel_path}"
    print(success_url, cancel_url)
    checkout_session = stripe.checkout.Session.create(
        line_items = [
            {
                "price": stripe_price_id,
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url=success_url,
        cancel_url=cancel_url
    )
    purchase.stripe_checkout_session_id = checkout_session.id
    purchase.save()
    return HttpResponseRedirect(checkout_session.url)

# def purchase_start_view(request):
#     if not request.method == 'POST':
#         return HttpResponseBadRequest()
#     if not request.user.is_authenticated:
#         return HttpResponseBadRequest()
#     handle = request.POST.get('handle')
#     obj = Product.objects.get(handle=handle)
#     stripe_price_id =  obj.stripe_price_id
#     if stripe_price_id is None :
#         return HttpResponseBadRequest()
    
#     purchase = Purchase.objects.create(user=request.user, product=obj)
#     request.session['purchase_id'] = purchase.id
#     success_path = reverse("purchases:success")
#     cancel_path = reverse("purchases:stopped")
#     success_url = f"{base_endpoint}/{success_path}"
#     cancel_url = f"{base_endpoint}/{cancel_path}"
#     if not success_path.startswith("/"):
#         success_path = f"{success_path}"
#     checkout_session = stripe.checkout.Session.create(
#         line_items=[
#             {
#                 'price': stripe_price_id,
#                 "quantity": 1,
#             }
#         ],
#         mode="payment",
#         success_url=success_url,
#         cancel_url=cancel_url
#     )
#     # number = random.randint(0,1)
#     # # if number == 1:
#     # #     return HttpResponseRedirect("/purchases/success")
#     # # else :
#     purchase.stripe_checkout_session_id = checkout_session.id
#     purchase.save()
#     return HttpResponseRedirect(checkout_session.url)

def purchase_success_view(request):
    purchase_id = request.session.get('purchase_id')
    if purchase_id:
        purchase = Purchase.objects.get(id=purchase_id)
        purchase.completed =True
        purchase.save()
        del request.session['purchase_id']
        return HttpResponseRedirect(purchase.product.get_absolute_url())
    return HttpResponse(f'Finished {purchase_id}')

def purchase_stopped_view(request):
    purchase_id = request.session.get('purchase_id')
    if purchase_id:
        purchase = Purchase.objects.get(id=purchase_id)
        product  =purchase.product
        return HttpResponseRedirect(product.get_absolute_url())
    return HttpResponse('Finished')
