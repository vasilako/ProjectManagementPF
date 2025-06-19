from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView
from .models import Product,Category

class ProductListView(ListView):
    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().select_related("category")
        category_id = self.request.GET.get("category")
        if category_id:
            queryset = queryset.filter(category__id=category_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        category_id = self.request.GET.get('category')
        context['selected_category'] = int(category_id) if category_id and category_id.isdigit() else None
        return context


