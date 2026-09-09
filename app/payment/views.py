import requests
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse
from .serializers import ZarinpalCallbackSerializer
from utils.gateways_zarinpal.zarinpal import ZarinpalGateway
from utils.gateways_zarinpal.services import complete_payment
from .models import PaymentModel, PaymentItemModel
from cart.models import CartProductModel, CartProductItemModel


class PaymentProductRequestAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        cart = get_object_or_404(CartProductModel.objects.select_related('user').select_for_update(), user=request.user)
        cart_item = list(cart.cart_items.select_related('product'))

        if not cart_item:
            return Response({"message": "سبد خرید خالی است."}, status=status.HTTP_400_BAD_REQUEST, )

        total_price = sum(item.product.price for item in cart_item)
        discount_amount = 0

        coupon = cart.coupon

        if coupon:
            if not coupon.is_valid:
                return Response({'message': 'کد تخفیف معتبر نیست.'}, status=status.HTTP_400_BAD_REQUEST)
            discount_amount = (total_price - coupon.discount) // 100

        amount_payable = total_price - discount_amount

        payment = PaymentModel.objects.create(
            user=request.user,
            amount=amount_payable,
            status=PaymentModel.Status.PENDING,
            coupon=coupon,
            discount_amount=discount_amount,
        )

        PaymentItemModel.objects.bulk_create([
            PaymentItemModel(
                payment=payment,
                product=item.product,
                price=item.product.price,
            )
            for item in cart_item
        ])

        callback_url = request.build_absolute_uri(reverse("payment:zarinpal-callback"))

        gateway = ZarinpalGateway()

        result = gateway.request_payment(
            amount=payment.amount,
            description=f' خرید {payment.id}',
            callback_url=callback_url,
            mobile=request.user.phone,
            email=request.user.email,
        )

        data = result.get('data', {})

        if data.get('code') != 100:
            payment.status = PaymentModel.Status.FAILED
            payment.save(update_fields=['status'])

            return Response(
                {
                    "detail": "ایجاد پرداخت در زرین‌پال ناموفق بود.",
                    "code": data.get("code"),
                    "message": data.get("message"),
                },
                status=status.HTTP_502_BAD_GATEWAY,
            )

        authority = data["authority"]
        payment.authority = authority
        payment.save(update_fields=["authority"])

        return Response(
            {
                "payment_id": payment.id,
                "amount": payment.amount,
                "authority": authority,
                "payment_url": gateway.get_payment_url(authority),
            },
            status=status.HTTP_201_CREATED,
        )


class ZarinpalCallbackAPIView(APIView):
    serializer_class = ZarinpalCallbackSerializer

    @extend_schema(
        parameters=[ZarinpalCallbackSerializer],
    )
    def get(self, request, *args, **kwargs):
        serializer = ZarinpalCallbackSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        authority = serializer.validated_data["Authority"]
        status_value = serializer.validated_data["Status"]

        payment = get_object_or_404(PaymentModel, authority=authority)

        if status_value != 'OK':
            payment.status = PaymentModel.Status.FAILED
            payment.save(update_fields=["status"])
            return Response({"message": "پرداخت توسط کاربر لغو یا ناموفق شد."}, status=status.HTTP_400_BAD_REQUEST, )

        if payment.status == PaymentModel.Status.SUCCESS:
            return Response({'message': 'این پرداخت قبلاً تایید شده است.'})

        gateway = ZarinpalGateway()

        try:

            result = gateway.verify_payment(amount=payment.amount, authority=authority)

        except requests.HTTPError:
            payment.status = PaymentModel.Status.FAILED
            payment.save(update_fields=["status"])
            return Response({'message': 'ارتباط با درگاه پرداخت برای تایید تراکنش ناموفق بود.'},
                            status=status.HTTP_401_UNAUTHORIZED)

        data = result.get("data", {})

        code = data.get("code")

        if code not in [100, 101]:
            payment.status = PaymentModel.Status.FAILED
            payment.save(update_fields=["status"])
            return Response(
                {
                    "detail": "پرداخت تایید نشد.",
                    "code": code,
                    "message": data.get("message"),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        reference_id = data.get("ref_id")

        complete_payment(payment=payment, reference_id=reference_id)

        return Response(
            {
                "detail": "پرداخت با موفقیت انجام شد.",
                "payment_id": payment.id,
                "reference_id": reference_id,
            }
        )


class PaymentStatusAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, payment_id):
        payment = get_object_or_404(PaymentModel, id=payment_id, user=request.user, )

        return Response({
            "payment_id": payment.id,
            "status": payment.status,
            "reference_id": payment.reference_id,
        })
