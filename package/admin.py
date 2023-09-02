from django.contrib import admin
from .models import Package
# Register your models here.


class PackageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'cost', 'status')
    list_filter = ('status', 'created', 'publish', 'user')


admin.site.register(Package, PackageAdmin)
