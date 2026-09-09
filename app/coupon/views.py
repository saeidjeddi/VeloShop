from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


from cart.models import CartProductModel, CartProductItemModel
from .models import CouponUsageModel, CouponModel
from .serializers import ApplyCouponSerializer



class ApplyCouponProductAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ApplyCouponSerializer

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serializer = ApplyCouponSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        code = serializer.validated_data['code']

        cart = (CartProductModel.objects.select_for_update().prefetch_related('cart_items__product').get(user=request.user))

        coupon = CouponModel.objects.filter(code=code, is_active=True).first()


        if not coupon:
            return Response({'detail': 'کد تخفیف معتبر نیست.'}, status=status.HTTP_400_BAD_REQUEST)

        if not coupon.is_valid:
            return Response({'detail': 'این کد تخفیف قابل استفاده نیست.'}, status=status.HTTP_400_BAD_REQUEST)

        if CouponUsageModel.objects.filter(user=request.user, coupon=coupon).exists():
            return Response({'message':'شما قبلاً از این کد تخفیف استفاده کرده‌اید.'  }, status=status.HTTP_400_BAD_REQUEST)

        if not cart.cart_items.exists():
            return Response({'detail': 'سبد خرید خالی است.'}, status=status.HTTP_400_BAD_REQUEST)

        cart.coupon = coupon
        cart.save(update_fields=['coupon', 'updated'])

        return Response(
            {
                'detail': 'کد تخفیف با موفقیت اعمال شد.',
                'code': coupon.code,
                'discount': coupon.discount,
            }, status=status.HTTP_200_OK)