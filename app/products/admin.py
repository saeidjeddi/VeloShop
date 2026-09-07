from django.contrib import admin
from django import forms
from django.db.models import Prefetch
from categories.models import ProductsCategoryModel

from .models import ProductModel, ProductAudioModel, ProductImageModel, ProductVideoModel


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = ProductModel
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["category"].queryset = (self.fields["category"].queryset.using("default"))



    def clean(self):
        cleaned_data = super().clean()

        self._validate_unique = False

        slug = cleaned_data.get("slug")

        if slug:
            exists = (
                ProductModel.objects
                .using("default")
                .filter(slug=slug)
                .exclude(pk=self.instance.pk)
                .exists()
            )

            if exists:
                self.add_error(
                    "slug",
                    "این slug قبلاً استفاده شده است.",
                )

        return cleaned_data


class ImageInline(admin.StackedInline):
    model = ProductImageModel
    extra = 1

    def get_queryset(self, request):
        return super().get_queryset(request).using("default")


class VideoInline(admin.StackedInline):
    model = ProductVideoModel
    extra = 1

    def get_queryset(self, request):
        return super().get_queryset(request).using("default")


class AudioInline(admin.StackedInline):
    model = ProductAudioModel
    extra = 1

    def get_queryset(self, request):
        return super().get_queryset(request).using("default")



class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm

    list_display = ('title', 'slug', 'price', 'is_active')
    search_fields = ['title', 'description', 'description_short']
    list_filter = ["is_active", "is_available", "is_special"]
    list_editable = ['is_active', 'price',]

    list_per_page = 10

    inlines = [
        ImageInline,
        VideoInline,
        AudioInline,
    ]

    filter_horizontal = ['category']

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .using("default")
            .prefetch_related(
                Prefetch(
                    "category",
                    queryset=ProductsCategoryModel.objects.using("default"),
                ),
                Prefetch(
                    "images",
                    queryset=ProductImageModel.objects.using("default"),
                ),
                Prefetch(
                    "videos",
                    queryset=ProductVideoModel.objects.using("default"),
                ),
                Prefetch(
                    "audios",
                    queryset=ProductAudioModel.objects.using("default"),
                ),
            )
        )
admin.site.register(ProductModel, ProductAdmin)
