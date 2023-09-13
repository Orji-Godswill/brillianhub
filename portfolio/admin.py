from django.contrib import admin
from .models import Land, Salary
# Register your models here.


class LandAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'bought_at', 'bought_year')


admin.site.register(Land, LandAdmin)


class SalaryAdmin(admin.ModelAdmin):
    list_display = ('month', 'sal_amount')


admin.site.register(Salary, SalaryAdmin)
