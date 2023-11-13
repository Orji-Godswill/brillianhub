from django.contrib.sitemaps import Sitemap
from .models import Course


class CourseSitemap(Sitemap):
    changefreg = 'weekly'
    priority = 0.8

    def items(self):
        return Course.objects.all().published()

    def lastmod(self, obj):
        return obj.publish
