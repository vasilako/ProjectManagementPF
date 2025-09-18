# payments/models.py


import uuid
from django.db import models
from django.utils import timezone

class PaymentQuote(models.Model):
    """
    Cotización cripto para una Order. Se usa para mostrar cantidad cripto al usuario
    y verificar luego que la tx on-chain cumple (>= amount_crypto).
    """
    quote_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    order = models.ForeignKey("orders.Order", on_delete=models.CASCADE, related_name="quotes")

    network = models.CharField(max_length=30)   # p.ej. "sepolia"
    symbol = models.CharField(max_length=10)    # p.ej. "ETH"
    amount_crypto = models.DecimalField(max_digits=36, decimal_places=18)
    receiving_address = models.CharField(max_length=64)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return timezone.now() < self.expires_at

    def __str__(self):
        return f"Quote {self.quote_id} · {self.symbol} {self.amount_crypto} · {self.network}"
