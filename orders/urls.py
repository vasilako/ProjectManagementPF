from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.checkout_cart, name='checkout_cart'),

]