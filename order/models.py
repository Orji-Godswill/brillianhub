from django.db import models
from brillianzhub.utils import unique_package_key_generator, unique_order_id_generator
from django.db.models.signals import pre_save, post_save
from django.conf import settings
from django.utils import timezone
from package.models import Package

ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('refunded', 'Refunded'),
    ('failed', 'Failed'),
)

PAYMENT_OPTION = (
    ('one_time_payment', 'One Time Payment'),
    ('installmental', 'Installmental')
)


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    referrer = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='referrer', on_delete=models.CASCADE, null=True, blank=True)
    order_id = models.CharField(max_length=50, blank=True, null=True)
    package = models.ForeignKey(
        Package, related_name='order_package', on_delete=models.CASCADE)
    slot = models.IntegerField(default=1)
    amount = models.DecimalField(default=0.00, max_digits=20, decimal_places=2)
    payment_option = models.CharField(
        max_length=50, default='one_time_payment', choices=PAYMENT_OPTION)
    payment_reference = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(
        max_length=50, default='created', choices=ORDER_STATUS_CHOICES)
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.order_id)

    def update_amount(self):
        package_amount = self.package.cost
        package_investor = self.package.investor
        self.amount = (package_amount / package_investor) * self.slot
        self.save()
        return package_amount

    def check_done(self):
        user = self.user
        amount = self.amount
        if user and amount > 0:
            return True
        return False

    def mark_paid(self):
        if self.check_done():
            self.status = 'paid'
            self.save()
        return self.status


def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)


pre_save.connect(pre_save_create_order_id, sender=Order)


def post_save_package_total(sender, instance, created, *args, **kwargs):
    if not created:
        package_obj = instance
        package_price = package_obj.cost
        package_id = package_obj.id
        qs = Order.objects.filter(package__id=package_id)
        if qs.count() == 1:
            order_obj = qs.first()
            order_obj.update_amount()


post_save.connect(post_save_package_total, sender=Package)


def post_save_order(sender, instance, created, *args, **kwargs):
    if created:
        instance.update_amount()


post_save.connect(post_save_order, sender=Order)
