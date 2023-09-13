from django.db import models
from django.conf import settings
# Create your models here.


class Land(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, blank=True, unique=True, null=True)
    description = models.CharField(max_length=150)
    location = models.CharField(max_length=50)
    bought_at = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.0)
    bought_year = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return str(self.name)


class Salary(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    month = models.CharField(max_length=15)
    sal_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    created = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return str(self.sal_amount)
