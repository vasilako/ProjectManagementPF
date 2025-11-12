# cart/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.translation import gettext as _
from decimal import Decimal
from products.models import Product


CART_SESSION_KEY = "cart"

# Create your views here.
def _get_cart(session):
    return session.setdefault(CART_SESSION_KEY, {})  # { "product_id_str": qty }


from decimal import Decimal
from django.shortcuts import render
from django.db.models import Prefetch
from products.models import Product  # ajusta el import según tu estructura

def cart_detail(request):
    """
    Renderiza el carrito con:
      - items: lista de dicts {product, qty, line_total}
      - total: suma de subtotales
      - total_items: suma de cantidades (no número de líneas)
    Optimiza consultas cargando todos los productos de una vez y
    prefetch de imágenes (relación 'images').
    """
    cart = _get_cart(request.session)  # dict {product_id(str/int): qty(int)}

    # Normaliza ids y filtra cantidades válidas (>0)
    pid_qty = {}
    for pid, qty in (cart or {}).items():
        try:
            ipid = int(pid)
            iqty = int(qty)
        except (TypeError, ValueError):
            continue
        if iqty > 0:
            pid_qty[ipid] = iqty

    items: list[dict] = []
    total = Decimal("0")
    total_items = 0

    if pid_qty:
        products = (
            Product.objects
            .filter(pk__in=pid_qty.keys())
            .prefetch_related("images")  # si tu relación es otra, cámbiala
        )
        pmap = {p.pk: p for p in products}

        # Conserva el orden de inserción del carrito
        for pid, qty in pid_qty.items():
            product = pmap.get(pid)
            if not product:
                continue  # producto eliminado o inexistente
            price = product.price if product.price is not None else Decimal("0")
            line_total = price * qty
            items.append({"product": product, "qty": qty, "line_total": line_total})
            total += line_total
            total_items += qty

    return render(
        request,
        "cart/detail.html",
        {"items": items, "total": total, "total_items": total_items},
    )


def cart_add(request, product_id):
    # Solo aceptar POST
    if request.method != "POST":
        return redirect("cart:cart_detail")

    product = get_object_or_404(Product, pk=product_id)

    # cantidad del form; si no viene, 1
    try:
        delta = int(request.POST.get("quantity", 1))
    except (TypeError, ValueError):
        delta = 1
    delta = max(1, delta)

    cart = _get_cart(request.session)
    pid = str(product_id)

    # cantidad acumulada
    new_qty = cart.get(pid, 0) + delta

    # (Opcional) límite por stock si existe product.stock
    if hasattr(product, "stock") and product.stock is not None:
        new_qty = min(new_qty, max(0, int(product.stock)))

    cart[pid] = new_qty
    request.session.modified = True

    messages.success(
        request,
        _("Added %(qty)d × %(name)s to your cart.") % {"qty": delta, "name": product.name}
    )

    # Volver a la ficha del producto si existe URL absoluta; si no, usar namespace de products
    if hasattr(product, "get_absolute_url") and product.get_absolute_url():
        return redirect(product.get_absolute_url())
    return redirect("products:product_detail", pk=product_id)


def cart_remove(request, product_id):
    if request.method != "POST":
        return redirect("cart:cart_detail")
    cart = _get_cart(request.session)
    pid = str(product_id)
    if pid in cart:
        cart.pop(pid)
        request.session.modified = True
        messages.info(request, _("Product removed from cart"))
    return redirect("cart:cart_detail")

def cart_update(request, product_id):
    """
       Cambia la cantidad de un producto ya en el carrito.
       Si se pone 0, elimina el producto.
       """
    product = get_object_or_404(Product, pk=product_id)
    try:
        qty = int(request.POST.get("quantity", 1))
    except (TypeError, ValueError):
        qty = 1

    cart = _get_cart(request.session)
    pid = str(product_id)

    if qty > 0:
        cart[pid] = qty
        messages.success(
            request,
            _("Updated %(name)s to %(qty)d units.") % {"qty": qty, "name": product.name}
        )
    else:
        cart.pop(pid, None)
        messages.info(request, _("Removed %(name)s from your cart.") % {"name": product.name})

    request.session.modified = True
    return redirect("cart:cart_detail")

