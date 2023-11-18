from rest_framework import serializers
from .models import Product, Favourite, Category


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class FavouritsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'