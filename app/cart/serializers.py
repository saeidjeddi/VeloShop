from rest_framework import serializers

from .models import CartProductItemModel


class CartProductItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source='product.id', read_only=True)
    title = serializers.CharField(source='product.title', read_only=True)
    slug = serializers.CharField(source='product.slug', read_only=True)
    image = serializers.ImageField(source='product.image', read_only=True)
    price = serializers.FloatField(source='product.price', read_only=True)

    class Meta:
        model = CartProductItemModel
        fields = ('product_id', 'title', 'slug', 'image', 'price',)



class CartProductItemAddSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
