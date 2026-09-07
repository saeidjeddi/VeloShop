from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status

from .models import ProductModel
from .serializers import ProductSerializer


class ProductListView(APIView):

    def get(self, request, *args, **kwargs):
        products = ProductModel.objects.using('replica').filter(is_active=True).prefetch_related('category', 'images', 'videos', 'audios')
        serializer = ProductSerializer(products, many=True, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)