from django.urls import path
from . import views

app_name = 'forum'

urlpatterns = [
    path('', views.lobby, name='index'),
    path('room/', views.room),
    path('get_token/', views.getToken),

    path('create_member/', views.createMember),
    path('get_member/', views.getMember),
    path('delete_member/', views.deleteMember),
]