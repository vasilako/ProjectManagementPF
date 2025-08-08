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

    STATUS_CHOICES = [
        (STATUS_PENDING, _('Pending')),
        (STATUS_PROCESSING, _('Processing')),
        (STATUS_SHIPPED, _('Shipped')),
        (STATUS_CANCELLED, _('Cancelled')),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    transaction_id = models.CharField(max_length=100, default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def __str__(self):
        return f"{_('Order')} #{self.id} – {self.user.email} – {self.get_status_display()}"

    def get_total(self):
        return sum(item.get_total_price() for item in self.items.all())


class OrderItem(models.Model):
    """
    Item of an order (product, quantity and unit price).
    """
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    class Meta:
        verbose_name = _('Order item')
        verbose_name_plural = _('Order items')

    def __str__(self):
        return f"{self.quantity} × {self.product.name} ({_('Order')} #{self.order.id})"

    def get_total_price(self):
        return self.price * self.quantity

    def save(self, *args, **kwargs):
        # Copy product price at time of creation
        if not self.price:
            self.price = self.product.price
        super().save(*args, **kwargs)
