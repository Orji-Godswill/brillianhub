from django.contrib import admin
from .models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'referrer', 'order_id', 'package',
                    'slot', 'amount', 'payment_option', 'status')


admin.site.register(Order, OrderAdmin)
# Register your models here.
