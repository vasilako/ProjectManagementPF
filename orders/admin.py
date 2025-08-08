from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Order, OrderItem
from .forms import OrderItemInlineForm


class ReadOnlyOrderItemInline(admin.TabularInline):
    model = OrderItem
    can_delete = False
    extra = 0
    readonly_fields = ('product', 'quantity', 'price')
    verbose_name = 'Order item'
    verbose_name_plural = 'Order items'

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    form = OrderItemInlineForm

    @admin.register(OrderItem)
    class OrderItemAdmin(admin.ModelAdmin):
        list_display = ('order', 'product_id_display', 'product_name_display', 'product_category_display', 'quantity',
                        'price')
        list_filter = ('product__category',)

        def product_id_display(self, obj):
            return obj.product.id

        product_id_display.short_description = 'Product ID'

        def product_name_display(self, obj):
            return obj.product.name

        product_name_display.short_description = 'Product Name'

        def product_category_display(self, obj):
            return obj.product.category.name

        product_category_display.short_description = 'Category'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display  = ('user',  'created_at', 'status_translated', 'calculated_total', 'id',)
    list_filter   = ('status', 'created_at')
    search_fields = ('user__email',)
    inlines       = [OrderItemInline]


    def get_readonly_fields(self, request, obj=None):
        # user SIEMPRE readonly, status NUNCA readonly
        return ('user', 'transaction_id', 'created_at')

    def get_inline_instances(self, request, obj=None):
        if obj and obj.status != 'pendiente':
            return [ReadOnlyOrderItemInline(self.model, self.admin_site)]
        return [OrderItemInline(self.model, self.admin_site)]

    def has_change_permission(self, request, obj=None):
        return True

    def status_translated(self, obj):
        return _(obj.get_status_display())
    status_translated.short_description = _('Status')

    def calculated_total(self, obj):
        return f"{obj.get_total():.2f} €"
    calculated_total.short_description = _('Total')



