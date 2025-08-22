from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from products.models import Product
import uuid

class Order(models.Model):
    """
    Represents an order placed by a user.
    """
    STATUS_PENDING = 'pendiente'
    STATUS_PROCESSING = 'procesando'
    STATUS_SHIPPED = 'enviado'
    STATUS_CANCELLED = 'cancelado'
    STATUS_PAID = 'pagado'  # ← nuevo estado de liquidación

    STATUS_CHOICES = [
        (STATUS_PENDING,    _('Pending')),
        (STATUS_PROCESSING, _('Processing')),
        (STATUS_SHIPPED,    _('Shipped')),
        (STATUS_CANCELLED,  _('Cancelled')),
        (STATUS_PAID,       _('Paid')),
    ]

    # Si quieres permitir invitados, haz null=True, blank=True y SET_NULL:
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)

    # UUID interno de pedido (no confundir con tx on-chain)
    transaction_id = models.CharField(max_length=100, default=uuid.uuid4, editable=False, unique=True)

    # --- Campos para conciliación cripto ---
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)  # EUR
    currency = models.CharField(max_length=8, default="EUR")

    network = models.CharField(max_length=32, blank=True, default="")           # p.ej. "sepolia"
    receiving_address = models.CharField(max_length=64, blank=True, default="")  # 0x...
    payment_tx_hash = models.CharField(max_length=80, blank=True, null=True)    # hash on-chain
    paid_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['transaction_id']),
            models.Index(fields=['payment_tx_hash']),
        ]

    def __str__(self):
        user_str = getattr(self.user, "email", "") if self.user_id else "guest"
        return f"{_('Order')} #{self.id} – {user_str} – {self.get_status_display()}"

    def get_total(self):
        return sum(item.get_total_price() for item in self.items.all())


class OrderItem(models.Model):
    """
    Item of an order (product, quantity and unit price).
    """
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    # permite None al crear, se rellena en save()
    price = models.DecimalField(max_digits=10, decimal_places=2, editable=False, null=True)

    class Meta:
        verbose_name = _('Order item')
        verbose_name_plural = _('Order items')

    def __str__(self):
        return f"{self.quantity} × {self.product.name} ({_('Order')} #{self.order.id})"

    def get_total_price(self):
        return (self.price or 0) * self.quantity

    def save(self, *args, **kwargs):
        # Copia precio de producto en el momento de creación
        if self.price is None:
            self.price = self.product.price
        super().save(*args, **kwargs)
