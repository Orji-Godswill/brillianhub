from django.contrib.sitemaps import Sitemap
from .models import Package


class PackageSitemap(Sitemap):
    changefreg = 'weekly'
    priority = 0.8

    def items(self):
        return Package.objects.all().published()

    def lastmod(self, obj):
        return obj.publish
