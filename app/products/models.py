from django.core.validators import MaxValueValidator
from django.db import models

from categories.models import ProductsCategoryModel


class ProductModel(models.Model):
    category = models.ManyToManyField(ProductsCategoryModel, related_name="products")
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    description_short = models.TextField(blank=True, null=True)
    price = models.PositiveBigIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=0)
    # discount = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(100)])
    is_active = models.BooleanField(default=True)
    is_available = models.BooleanField(default=True)
    is_special = models.BooleanField(default=False)
    most_viewed = models.PositiveIntegerField(default=0)
    sales = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "products"
        indexes = [
            models.Index(fields=["title", "slug", "is_active", "is_available", "is_special", "most_viewed", "sales", "created_at"]),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class ProductImageModel(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="products/images/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "products_image"
        ordering = ["-created_at"]

    def __str__(self):
        return self.product.title


class ProductVideoModel(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name="videos")
    video = models.FileField(upload_to="products/videos/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "products_video"
        ordering = ["-created_at"]

    def __str__(self):
        return self.product.title


class ProductAudioModel(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name="audios")
    audio = models.FileField(upload_to="products/audios/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "products_audio"
        ordering = ["-created_at"]

    def __str__(self):
        return self.product.title
