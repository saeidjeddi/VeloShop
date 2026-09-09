from django.db import models
from django.conf import settings

from coupon.models import CouponModel
from products.models import ProductModel



class PaymentModel(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'در انتظار پرداخت'
        SUCCESS = 'success', 'موفق'
        FAILED = 'failed', 'ناموفق'
        EXPIRED = 'expired', 'منقضی شده'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='payment_user')
    amount = models.PositiveBigIntegerField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    authority = models.CharField(max_length=255, null=True, blank=True, unique=True)
    reference_id = models.CharField(max_length=255, null=True, blank=True, unique=True)
    coupon = models.ForeignKey(CouponModel, on_delete=models.PROTECT, null=True, blank=True, related_name='payment_coupon',)
    discount_amount = models.PositiveBigIntegerField(default=0,)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Payment #{self.user.username}'

    class Meta:
        db_table = 'payment'
        ordering = ['-created_at']


class PaymentItemModel(models.Model):
    payment = models.ForeignKey(PaymentModel, on_delete=models.PROTECT, related_name='items_payment')
    product = models.ForeignKey(ProductModel, on_delete=models.PROTECT, related_name='items_product')
    price = models.PositiveBigIntegerField()

    class Meta:
        db_table = 'payment_item'

        constraints = [
            models.UniqueConstraint(
                fields=['payment', 'product'],
                name='unique_product_per_payment',
            )
        ]

    def __str__(self):
        return f'{self.payment.user.username} - {self.product.title}'