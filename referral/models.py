from django.db import models
from django.conf import settings

# Create your models here.


class Referrer(models.Model):
    referrer = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='referrer_user', on_delete=models.CASCADE)
    referred = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='referred', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.referrer)


class Earn(models.Model):
    referrer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    earn = models.CharField(max_length=100, null=True, blank=True)
    balance = models.DecimalField(
        default=0.00, max_digits=20, decimal_places=2)
    withdrawn = models.DecimalField(
        default=0.00, max_digits=20, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.referrer)


class Payout(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField()
    amount = models.DecimalField(default=0.00, max_digits=20, decimal_places=2)
    paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)
