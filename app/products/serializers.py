from rest_framework import serializers

from .models import (
    ProductModel,
    ProductImageModel,
    ProductVideoModel,
    ProductAudioModel,
)

from categories.serializers import ProductsCategorySerializer


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImageModel
        fields = ("id", "image_slider")

class ProductVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVideoModel
        fields = ("id", "video")


class ProductAudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAudioModel
        fields = ("id", "audio")

class ProductListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = ProductModel
        fields = ['id', 'title','image', 'slug', 'description_short', 'price', 'is_available']

    def get_image(self, obj):
        if not obj.image:
            return None

        request = self.context.get('request')

        if request:
            return request.build_absolute_uri(obj.image.url)

        return obj.image.url






class ProductDetailSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    videos = ProductVideoSerializer(many=True, read_only=True)
    audios = ProductAudioSerializer(many=True, read_only=True)
    categories = ProductsCategorySerializer(many=True, read_only=True, source="category",)

    class Meta:
        model = ProductModel
        fields = [
            "id",
            "categories",
            "title",
            "image",
            "slug",
            "description",
            "description_short",
            "price",
            "quantity",
            "is_active",
            "is_available",
            "is_special",
            "most_viewed",
            "sales",
            "images",
            "videos",
            "audios",
            "created_at",
            "updated_at",
        ]

