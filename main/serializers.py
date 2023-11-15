from rest_framework import serializers
from .models import Product,  Category


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class QuerySerializer(serializers.Serializer):
    query = serializers.CharField()


