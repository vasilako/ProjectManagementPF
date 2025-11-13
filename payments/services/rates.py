# ./payments/services/rates.py


from decimal import Decimal
import requests, time

_cache = {"t": 0, "ETH": None}

def get_rate_eur_eth() -> Decimal:
    # Retorna EUR por 1 ETH
    now = time.time()
    if now - _cache["t"] < 30 and _cache["ETH"] is not None:
        return _cache["ETH"]
    r = requests.get(
        "https://api.coingecko.com/api/v3/simple/price",
        params={"ids":"ethereum","vs_currencies":"eur"},
        timeout=5,
    )
    price_eur = Decimal(str(r.json()["ethereum"]["eur"]))
    _cache["t"] = now
    _cache["ETH"] = price_eur
    return price_eur

def eur_to_eth(eur: Decimal, buffer_pct: Decimal) -> Decimal:
    # Convierte EUR a ETH aplicando colchón (%), redondeo HACIA ARRIBA a 18 dec.
    price = get_rate_eur_eth()       # EUR / ETH
    raw = eur / price                # ETH
    with_buffer = raw * (Decimal("1") + buffer_pct)
    return with_buffer.quantize(Decimal("0.000000000000000001"))
