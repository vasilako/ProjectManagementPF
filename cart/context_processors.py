# cart/contex_processors.py

from products.models import Product

def cart_summary(request):
    cart = request.session.get("cart", {})
    total_items, total_price = 0, 0
    for pid, qty in cart.items():
        try:
            p = Product.objects.get(pk=int(pid))
            total_items += qty
            total_price += (p.price or 0) * qty
        except Product.DoesNotExist:
            continue
    return {"cart_total_items": total_items, "cart_total_price": total_price}
