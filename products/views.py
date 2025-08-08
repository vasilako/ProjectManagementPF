from django.views.generic import ListView
from django.views.generic.detail import DetailView
from .models import Product,Category
from django.utils.translation import gettext as _


import logging

logger = logging.getLogger(__name__)

# Create your views here.

class ProductListView(ListView):
    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"
    paginate_by = 8

    def get_queryset(self):
        queryset = super().get_queryset().select_related("category").order_by("name")
        logger.debug(f"Logging Queryset: {queryset}")

        category_id = self.request.GET.get("category")
        if category_id:
            queryset = queryset.filter(category__id=category_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        category_id = self.request.GET.get('category')
        context['selected_category'] = int(category_id) if category_id and category_id.isdigit() else None
        context['page_title'] = _("Product List")  # Marked chain for translation
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = "products/product_detail.html"
    context_object_name = "product"