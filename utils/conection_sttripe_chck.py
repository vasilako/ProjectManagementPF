import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

try:
    account = stripe.Account.retrieve()
    print("✅ Conexión a Stripe OK")
    print(f"Cuenta: {account['email']} (ID: {account['id']})")
except stripe.error.AuthenticationError:
    print("❌ Clave API incorrecta o no válida.")
except Exception as e:
    print(f"❌ Error general al conectar con Stripe: {e}")
