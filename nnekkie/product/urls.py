from django.urls import path

from .views import *

app_name='product'

urlpatterns = [
    path('create/', create_product_view, name='create'),
    path('purchased/', purchased, name='purchased'),
    path('', product_list_view, name='list'),
    path('search-product/', search_product, name='product-search'),
    path('<slug:handle>/', product_detail_view, name='detail'),
    path('<slug:handle>/manage/',product_manage_detail_view , name='manage'),
    path('<slug:handle>/download/<int:pk>', product_attachment_view, name='download')
]