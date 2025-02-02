from django.urls import path

from .views import *

app_name='purchases'

urlpatterns = [
    path('start/', purchase_start_view, name='start'),
    path('success/', purchase_success_view, name='success'),
    path('stopped/', purchase_stopped_view, name='stopped'),
  
]