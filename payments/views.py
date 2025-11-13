# payments/views.py
import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required

from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_GET


from orders.models import Order


CART_SESSION_KEY = "cart"
def _get_cart(session):
    return session.setdefault(CART_SESSION_KEY, {})  # { "product_id_str": qty }


stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def create_stripe_checkout_session(request, order_id):
    user = request.user
    order = get_object_or_404(Order, pk=order_id)

    if order.status != Order.STATUS_PENDING:
        return HttpResponseBadRequest("Order not pending")

    lang = request.LANGUAGE_CODE
    # success_url = f"{settings.STRIPE_DOMAIN}{reverse('payments:stripe_success')}?session_id={{CHECKOUT_SESSION_ID}}"
    success_url = (
        f"{settings.STRIPE_DOMAIN}"
        f"{reverse('payments:stripe_success')}"
        f"?session_id={{CHECKOUT_SESSION_ID}}&order_id={order.id}"
    )

    cancel_url = f"{settings.STRIPE_DOMAIN}{reverse('payments:stripe_cancel')}"

    line_items = [
        {
            "price_data": {
                "currency": "eur",
                "product_data": {"name": item.product.name},
                "unit_amount": int(item.price * 100),
            },
            "quantity": item.quantity,
        }
        for item in order.items.all()
    ]

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            mode="payment",
            success_url=success_url,
            cancel_url=cancel_url,
            billing_address_collection="auto",
            customer_email=user.email,  # ✅ solo usamos el email
            metadata={"order_id": order.id},
            payment_method_options={
                "card": {
                    "setup_future_usage": None
                }
            }
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({"ok": True, "url": session.url})
    return redirect(session.url)



@login_required
@require_GET
def stripe_success(request):
    order_id = request.GET.get("order_id")
    if not order_id:
        raise Http404("ID de pedido no proporcionado.")

    # ✅ Buscar el pedido y asegurar que sea del usuario
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # ✅ Limpiar el carrito de la sesión
    if CART_SESSION_KEY in request.session:
        del request.session[CART_SESSION_KEY]

    return render(request, "payments/success.html", {"order": order})


@login_required
@require_GET
def stripe_cancel(request):
    return render(request, "payments/cancel.html")
