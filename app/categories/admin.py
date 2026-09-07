from django import forms
from django.contrib import admin

from .models import ProductsCategoryModel



class ProductAdminForm(forms.ModelForm):

    class Meta:
        model = ProductsCategoryModel
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["parent"].queryset = (
            ProductsCategoryModel.objects
            .using("default")
            .all()
        )

    def clean(self):
        cleaned_data = super().clean()

        # جلوگیری از unique validation خودکار
        # چون ممکن است Router آن را به replica بفرستد.
        self._validate_unique = False

        slug = cleaned_data.get("slug")

        if slug:
            exists = (
                ProductsCategoryModel.objects
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




@admin.register(ProductsCategoryModel)
class ProductsCategoryModelAdmin(admin.ModelAdmin):
    form = ProductAdminForm

    list_display = ("title", "slug", "created_at", "updated_at")
    search_fields = ("title", "slug")
    list_filter = ("created_at", "updated_at")
    list_per_page = 10

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .using("default")
        )

    def save_model(self, request, obj, form, change):
        obj.save(using="default")