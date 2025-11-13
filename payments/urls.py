# payments/urls.py
from django.urls import path
from . import views

app_name = "payments"

urlpatterns = [
    path("stripe/checkout/<int:order_id>/", views.create_stripe_checkout_session, name="stripe_checkout"),
    path("success/", views.stripe_success, name="stripe_success"),
    path("cancel/", views.stripe_cancel, name="stripe_cancel"),

]
