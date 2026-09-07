import django_filters

from .models import ProductsCategoryModel



class ProductsCategoryFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='istartswith')
    parent = django_filters.CharFilter(field_name="parent__title",lookup_expr="icontains")
    class Meta:
        model = ProductsCategoryModel
        fields = ['parent', 'title']