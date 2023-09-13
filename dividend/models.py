from django.db import models
from django.db.models.query import QuerySet
from package.models import Package
from django.conf import settings
# Create your models here.


class Dividend(models.Model):
    package = models.ForeignKey(
        Package, related_name="package_dividend", on_delete=models.CASCADE)
    amount = models.DecimalField(default=0.00, max_digits=20, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    income = models.Manager()

    def __str__(self):
        return str(self.package)
