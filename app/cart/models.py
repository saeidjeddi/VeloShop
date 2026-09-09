from django.db import models
from django.conf import settings

from coupon.models import CouponModel
from products.models import ProductModel


class CartProductModel(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart_user')
    coupon = models.ForeignKey(CouponModel, on_delete=models.SET_NULL, related_name='coupon_cart', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.user.username


    class Meta:
        db_table = 'cart_model'
        ordering = ['-created']


class CartProductItemModel(models.Model):
    cart = models.ForeignKey(CartProductModel, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='product_items')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.title

    class Meta:
        db_table = 'cart_item'
        ordering = ['-created']

        constraints = [
            models.UniqueConstraint(fields=['product', 'cart'], name='unique_cart_item')
        ]
