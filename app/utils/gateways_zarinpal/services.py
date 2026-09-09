from django.db import transaction
from django.utils import timezone
from products.models import ProductModel
from payment.models import PaymentModel
from coupon.models import CouponModel, CouponUsageModel
from cart.models import CartProductModel


@transaction.atomic
def complete_payment(payment, reference_id):
    payment = (PaymentModel.objects.select_for_update().get(pk=payment.pk))

    if payment.status == PaymentModel.Status.SUCCESS:
        return

    payment.status = PaymentModel.Status.SUCCESS
    payment.reference_id = reference_id
    payment.paid_at = timezone.now()

    payment.save(update_fields=['status', 'reference_id', 'paid_at'])



    if payment.coupon_id:
        coupon = CouponModel.objects.select_for_update().get(pk=payment.coupon_id)
        CouponUsageModel.objects.create(coupon=coupon, user=payment.user)
        coupon.used_count +=  1
        coupon.save(update_fields=['used_count'])


    items = list(payment.items_payment.select_related('product'))
    for item in items:
        item.product.sales += 1
        item.product.save(update_fields=['sales'])

    cart = CartProductModel.objects.select_related('user', 'coupon').filter(user=payment.user).first()

    if cart:
        product_ids = payment.items_payment.values_list('product_id', flat=True)
        cart.cart_items.filter(product_id__in=product_ids).delete()
        cart.coupon = None
        cart.save(update_fields=['coupon', 'updated'])


