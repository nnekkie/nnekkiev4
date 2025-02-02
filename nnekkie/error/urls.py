from django.urls import path
from .views import *


app_name = 'error'
urlpatterns = [
    path('404/', handler404),
    path('403/', handler403),
    path('400/', handler400),
    path('500/', handler500),
]