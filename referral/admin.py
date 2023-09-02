from django.contrib import admin
from .models import Referrer
# Register your models here.


class ReferrerAdmin(admin.ModelAdmin):
    display_list = ('referrer', 'referred', 'created')


admin.site.register(Referrer, ReferrerAdmin)
