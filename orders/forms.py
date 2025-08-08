from django import forms
from .models import OrderItem
from products.models import Product


class OrderItemInlineForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].label_from_instance = lambda obj: f"Category ({obj.category.name}), Product ({obj.name}), (ID: {obj.id})"
