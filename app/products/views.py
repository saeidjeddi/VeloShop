from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.core.cache import cache
from rest_framework import status
from django.db import models
from config.settings import PRODUCT_CACHE_VERSION_KEY
from utils.customPagination import CustomPagination
from .models import ProductModel
from .serializers import ProductListSerializer, ProductDetailSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter

class ProductListView(APIView):

    # filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter
    pagination_class = CustomPagination
    CACHE_TIMEOUT = 60 * 1

    def get(self, request, format=None):
        version = cache.get(PRODUCT_CACHE_VERSION_KEY, 1)
        cache_key = f"products:list:v{version}:{request.get_full_path()}"
        cached_response = cache.get(cache_key)
        if cached_response is not None:

            return Response(cached_response)


        queryset = ProductModel.objects.filter(is_active=True)
        filterset = self.filterset_class(data=request.query_params, queryset=queryset)
        if filterset.is_valid():
            queryset = filterset.qs
            paginator = self.pagination_class()
            page = paginator.paginate_queryset(queryset, request)
            serializer = ProductListSerializer(page, many=True, context={'request': request})
            response = paginator.get_paginated_response(serializer.data)
            cache.set(cache_key,response.data,self.CACHE_TIMEOUT)
            return response
        return Response(filterset.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailView(APIView):
    serializer_class = ProductDetailSerializer
    CACHE_TIMEOUT = 60 * 1

    def get(self, request, pk, slug,*args, **kwargs):
        version = cache.get(PRODUCT_CACHE_VERSION_KEY,1)
        cache_key = (f"products:detail:v{version}:{pk}:{slug}",)
        cached_response = cache.get(cache_key)
        if cached_response is not None:
            # ProductModel.objects.filter(pk=pk,is_active=True).update(most_viewed=models.F("most_viewed") + 1)
            return Response(cached_response)

        product = get_object_or_404(ProductModel.objects.filter(is_active=True).prefetch_related('category','images', 'videos', 'audios'), pk=pk, slug=slug)
        ProductModel.objects.filter(pk=product.pk).update(most_viewed=models.F("most_viewed") + 1)
        serializer = ProductDetailSerializer(product, context={'request': request})
        cache.set(cache_key,serializer.data,self.CACHE_TIMEOUT)
        return Response(serializer.data)