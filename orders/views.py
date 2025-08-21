from django.shortcuts import render

# Create your views here.
def checkout_cart(request):
    return render(request, "orders/checkout.html")

