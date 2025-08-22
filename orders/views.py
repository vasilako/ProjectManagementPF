from decimal import Decimal
from time import sleep
import datetime, json

from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_GET, require_POST  # ← AÑADIR

from products.models import Product
from .models import Order, OrderItem
from payments.models import PaymentQuote
from payments.services.rates import eur_to_eth
from web3 import Web3


def _get_cart(session):
    return session.setdefault("cart", {})


def checkout_cart(request):
    cart = _get_cart(request.session)
    if not cart:
        return redirect("cart:cart_detail")

    # Calcula líneas y total
    items, total = [], Decimal("0")
    for pid, qty in cart.items():
        p = Product.objects.get(pk=int(pid))
        qty = int(qty)
        line = (p.price or Decimal("0")) * qty
        items.append((p, qty, line)); total += line

    # Recupera order de sesión si existe
    order = None
    order_id = request.session.get("order_id")
    if order_id:
        order = Order.objects.filter(pk=order_id).first()

    # Si no existe o no está pendiente → crea una nueva
    if not order or order.status != Order.STATUS_PENDING:
        net = settings.CRYPTO_NETWORKS["sepolia"]
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            status=Order.STATUS_PENDING,
            total_amount=total,
            currency="EUR",
            network="sepolia",
            receiving_address=net["receiving_address"],
        )
        for p, qty, _line in items:
            OrderItem.objects.create(order=order, product=p, quantity=qty, price=p.price)
        request.session["order_id"] = order.id

    return render(request, "orders/checkout.html", {"order": order, "items": items, "total": total})


@require_GET
def create_quote(request, order_id):
    order = Order.objects.filter(pk=order_id).first()
    if not order:
        return JsonResponse({"ok": False, "error": "order_not_found"}, status=404)
    if order.status != Order.STATUS_PENDING:
        return JsonResponse({"ok": False, "error": "order_not_pending"}, status=409)

    net = settings.CRYPTO_NETWORKS["sepolia"]
    amount_crypto = eur_to_eth(Decimal(order.total_amount), Decimal(str(settings.CRYPTO_PRICE_BUFFER_PCT)))
    expires_at = timezone.now() + datetime.timedelta(seconds=settings.CRYPTO_QUOTE_TTL_SECONDS)

    q = PaymentQuote.objects.create(
        order=order, network="sepolia", symbol=net["symbol"],
        amount_crypto=amount_crypto, receiving_address=net["receiving_address"],
        expires_at=expires_at,
    )
    return JsonResponse({
        "ok": True,
        "quote_id": str(q.quote_id),
        "symbol": q.symbol,
        "chain_id": net["chain_id"],
        "amount_crypto": str(q.amount_crypto),
        "receiving_address": q.receiving_address,
        "expires_at": expires_at.isoformat(),
    })


@require_POST
def confirm_payment(request):
    # Recibe {order_id, txHash} desde el front y verifica on-chain
    if request.method != "POST":
        return HttpResponseBadRequest("POST only")

    try:
        data = json.loads(request.body.decode())
        order_id = int(data["order_id"])
        tx_hash = data["txHash"]
    except Exception:
        return HttpResponseBadRequest("bad payload")

    order = Order.objects.get(pk=order_id)
    net = settings.CRYPTO_NETWORKS[order.network or "sepolia"]

    # Última cotización (vigente) de la order
    quote = (
        PaymentQuote.objects
        .filter(order=order)
        .order_by("-created_at")
        .first()
    )
    if not quote or not quote.is_valid():
        return JsonResponse({"ok": False, "error": "quote_missing_or_expired"})

    expected_wei = int(Decimal(quote.amount_crypto) * (10 ** net["decimals"]))

    # Verificación on-chain con web3.py + Alchemy
    w3 = Web3(Web3.HTTPProvider(net["rpc_url"]))

    # Esperar a que la tx exista/mina (con backoff simple)
    receipt = None
    elapsed = 0
    timeout = getattr(settings, "PAYMENT_VERIFY_TIMEOUT", 90)
    poll = getattr(settings, "PAYMENT_VERIFY_POLL", 3)

    while elapsed < timeout:
        try:
            receipt = w3.eth.get_transaction_receipt(tx_hash)
            if receipt:  # cuando hay receipt, la tx ya está incluida en un bloque
                break
        except Exception:
            pass
        sleep(poll)
        elapsed += poll

    if not receipt:
        # Aún no hay receipt: indica al front que siga intentando (no marcar error definitivo)
        return JsonResponse({"ok": False, "pending": True, "error": "tx_pending"})



    # Ya hay receipt: traemos también la tx para verificar 'to' y 'value'
    try:
        tx = w3.eth.get_transaction(tx_hash)
        receipt = w3.eth.get_transaction_receipt(tx_hash)
    except Exception as e:
        return JsonResponse({"ok": False, "error": f"rpc_error: {e}"})


    ok_basic = (
        tx and receipt and receipt["status"] == 1 and
        tx["to"] and tx["to"].lower() == (order.receiving_address or net["receiving_address"]).lower() and
        int(tx["value"]) >= expected_wei
    )
    if not ok_basic:
        return JsonResponse({"ok": False, "error": "tx_mismatch"})

    # (Opcional) confirmaciones mínimas (Sepolia: >=1)
    # current_block = w3.eth.block_number
    # if current_block - receipt["blockNumber"] < 1:
    #     return JsonResponse({"ok": False, "error": "not_enough_confirmations"})

    # Marcar Order como pagada
    order.status = Order.STATUS_PAID
    order.payment_tx_hash = tx_hash
    order.paid_at = timezone.now()
    order.save()

    # Vaciar carrito
    request.session["cart"] = {}

    return JsonResponse({"ok": True})


def confirm_page(request):
    return render(request, "orders/confirm.html", {"id": request.GET.get("id")})
