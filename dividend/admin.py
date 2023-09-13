from django.contrib import admin
from .models import Dividend
# Register your models here.


class DividendAdmin(admin.ModelAdmin):
    list_display = ('package', 'amount', 'created')


admin.site.register(Dividend, DividendAdmin)
