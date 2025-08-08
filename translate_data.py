# translate_data.py
import requests
from products.models import Product, Category

def translate_text(text, target_lang='es'):
    if not text:
        return text
    endpoint = 'http://localhost:5000/translate'
    payload = {
        'q': text,
        'source': 'en',
        'target': target_lang,
        'format': 'text'
    }
    try:
        response = requests.post(endpoint, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()['translatedText']
    except requests.RequestException as e:
        print(f"Error traduciendo '{text}': {e}")
        return text

# Traducir categorías
for category in Category.objects.all():
    if category.name_en and not category.name_es:
        category.name_en = category.name
        category.name_es = translate_text(category.name, 'es')
    if category.description_en and not category.description_es:
        category.description_es = translate_text(category.description_en, 'es')
    category.save()
    print(f"Traducido Category: {category.name} -> {category.name_es}")

# Traducir productos
# for product in Product.objects.all():
#     if product.name_en and not product.name_es:
#         product.name_es = translate_text(product.name_en, 'es')
#     if product.description_en and not product.description_es:
#         product.description_es = translate_text(product.description_en, 'es')
#     product.save()
#     print(f"Traducido Product: {product.name_en} -> {product.name_es}")