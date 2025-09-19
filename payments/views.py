# payments/views.py
import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required

from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse, HttpResponseBadRequest

from orders.models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def create_stripe_checkout_session(request, order_id):
    order = get_object_or_404(Order, pk=order_id)

    # Asegurar que la orden está pendiente
    if order.status != Order.STATUS_PENDING:
        return HttpResponseBadRequest("Order not pending")

    # Construir URLs con idioma activo
    lang = request.LANGUAGE_CODE

    success_url = f"{settings.STRIPE_DOMAIN}{reverse('payments:stripe_success')}?session_id={{CHECKOUT_SESSION_ID}}"
    cancel_url = f"{settings.STRIPE_DOMAIN}{reverse('payments:stripe_cancel')}"

    # Generar line_items desde OrderItems
    line_items = []
    for item in order.items.all():
        line_items.append({
            "price_data": {
                "currency": "eur",
                "product_data": {
                    "name": item.product.name,
                },
                "unit_amount": int(item.price * 100),
            },
            "quantity": item.quantity,
        })

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            mode="payment",
            success_url=success_url,
            cancel_url=cancel_url,
            metadata={"order_id": order.id}
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

    # Devuelve JSON si es fetch/AJAX, si no redirige
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({"ok": True, "url": session.url})
    return redirect(session.url)


def stripe_success(request):
    return render(request, "payments/success.html")


def stripe_cancel(request):
    return render(request, "payments/cancel.html")
