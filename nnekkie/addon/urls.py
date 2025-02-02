from django.urls import path

from . import views

app_name = 'addon'

urlpatterns = [
    path('', views.page_index, name='page-index')
]