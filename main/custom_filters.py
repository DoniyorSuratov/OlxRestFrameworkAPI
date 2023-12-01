from django_filters import rest_framework as filters
# from rest_framework import filters
from main.models import Product


class ProductFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Product
        fields = ( 'slug', 'expires_at', 'category', 'title', 'color', 'price')
