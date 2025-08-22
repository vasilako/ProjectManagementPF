from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("checkout/", views.checkout_cart, name="checkout_cart"),
    path("quote/<int:order_id>/", views.create_quote, name="create_quote"),
    path("confirm_payment/", views.confirm_payment, name="confirm_payment"),
    path("confirm/", views.confirm_page, name="confirm"),
]
