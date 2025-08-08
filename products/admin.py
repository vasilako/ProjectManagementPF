from django.contrib import admin
from .models import Category, Product, ProductImage


# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "price")
    inlines = [ProductImageInline]
    search_fields = ("name", "description",)
    list_filter = ("category",)


