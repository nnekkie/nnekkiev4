from django.urls import path
from .views import *

app_name = 'grc'


urlpatterns = [
    path('<slug:slug>/', index, name='index')
]