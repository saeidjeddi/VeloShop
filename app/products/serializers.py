from rest_framework import serializers

from .models import (
    ProductModel,
    ProductImageModel,
    ProductVideoModel,
    ProductAudioModel,
)


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImageModel
        fields = ("id", "image")

class ProductVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVideoModel
        fields = ("id", "video")


class ProductAudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAudioModel
        fields = ("id", "audio")


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    videos = ProductVideoSerializer(many=True, read_only=True)
    audios = ProductAudioSerializer(many=True, read_only=True)

    class Meta:
        model = ProductModel
        fields = [
            "id",
            "category",
            "title",
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

