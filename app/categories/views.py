from rest_framework import status
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import ProductsCategorySerializer
from .models import ProductsCategoryModel
from .filters import ProductsCategoryFilter
from products.serializers import ProductListSerializer
from products.models import ProductModel
from products.filters import ProductFilter
from utils.customPagination import CustomPagination
from rest_framework.response import Response
from django.core.cache import cache

from config.settings import CATEGORY_CACHE_VERSION_KEY


class CategoryView(ListAPIView):
    serializer_class = ProductsCategorySerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductsCategoryFilter
    CACHE_TIMEOUT = 60 * 5

    def get(self, request, *args, **kwargs):
        version = cache.get(CATEGORY_CACHE_VERSION_KEY, 1)
        cache_key = (f"categories:list:v{version}:{request.get_full_path()}",)
        cached_response = cache.get(cache_key)
        if cached_response is not None:
            return Response(cached_response, status=status.HTTP_200_OK)

        response = super().get(request, *args, **kwargs)

        cache.set(cache_key, response.data, timeout=self.CACHE_TIMEOUT)
        return response

    def get_queryset(self, ):
        return ProductsCategoryModel.objects.select_related("parent").all()


class ProductsCategoryView(ListAPIView):
    serializer_class = ProductListSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter
    CACHE_TIMEOUT = 60 * 5

    def get(self, request, *args, **kwargs):
        version = cache.get(CATEGORY_CACHE_VERSION_KEY, 1)
        category_id = kwargs["category_id"]

        cache_key = (f"categories:products:v{version}:{category_id}:{request.get_full_path()}",)
        cached_response = cache.get(cache_key)

        if cached_response is not None:
            return Response(cached_response)

        response = super().get(request, *args, **kwargs)

        cache.set(cache_key, response.data, timeout=self.CACHE_TIMEOUT)

        return response

    def get_queryset(self, ):
        category_id = self.kwargs["category_id"]
        return ProductModel.objects.filter(category__id=category_id)
