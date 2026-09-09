from itertools import product

from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import CartProductItemModel, CartProductModel
from products.models import ProductModel
from .serializers import CartProductItemSerializer


class CartProductItemView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartProductItemSerializer

    def get(self, request):
        cart, created  = CartProductModel.objects.select_related("user", "coupon").get_or_create(user=request.user)
        items = list(cart.cart_items.select_related("product"))
        serializer = CartProductItemSerializer(items, many=True, context={'request': request})

        coupon = cart.coupon

        discount_percent = 0

        if coupon and coupon.is_valid:
            discount_percent = coupon.discount

        total_price = sum(item.product.price for item in items)

        amount = (total_price * discount_percent // 100 )

        amount_payable = total_price - amount

        return Response({
            'message' :'سبد خرید کاربر : قیمت ها به تومان هست',
            'user': cart.user.username,
            'items': serializer.data,
            'total_price': total_price,
            'discount_percent' : discount_percent,
            'amount': amount,
            'amount_payable' : amount_payable
        },status=status.HTTP_200_OK)



class CartProductItemRemoveAddView(APIView):

    def post(self, request, pk, *args, **kwargs):
        product = get_object_or_404(ProductModel.objects.prefetch_related("category", "audios", "videos", "images"), is_active=True, pk=pk)
        cart, created = CartProductModel.objects.select_related("user").get_or_create(user=request.user)

        if CartProductItemModel.objects.select_related('cart', 'product').filter(cart=cart, product=product).exists():
            return Response({'message': 'این محصول قبلا در سبد خرید شما وجود دارد'}, status=status.HTTP_400_BAD_REQUEST)

        if cart.cart_items.count() >= 5:
            return Response({"message": "سبد خرید نمی‌تواند بیشتر از 5 محصول داشته باشد"}, status=status.HTTP_400_BAD_REQUEST)

        cart_item = CartProductItemModel.objects.select_related('cart', 'product').create(cart=cart, product=product)

        return Response(CartProductItemSerializer(cart_item, context={'request': request}).data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk, *args, **kwargs):
        cart = get_object_or_404(CartProductModel.objects.select_related("user"))
        cart_item = get_object_or_404(CartProductItemModel.objects.select_related("cart", "product"), product_id=pk, cart=cart)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



