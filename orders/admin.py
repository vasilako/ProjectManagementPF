from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    verbose_name = _('Order item')
    verbose_name_plural = _('Order items')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status_translated', 'created_at', 'total_price')
    list_filter = ('status', 'created_at')
    inlines = [OrderItemInline]
    search_fields = ('user__email',)

    def status_translated(self, obj):
        return _(obj.get_status_display())
    status_translated.short_description = _('Status')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')
    list_filter = ('product',)
