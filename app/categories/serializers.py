from rest_framework import serializers
from .models import ProductsCategoryModel

class ProductsParentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductsCategoryModel
        fields = ["id", "title", "slug"]


class ProductsCategorySerializer(serializers.ModelSerializer):
    parents = ProductsParentCategorySerializer(read_only=True)
    class Meta:
        model = ProductsCategoryModel
        fields = ["id", "title", "slug", "parents"]