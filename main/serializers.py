from rest_framework import serializers
from .documents import DocumentProduct
from .models import Product, Favourite, Category
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class FavouritsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = '__all__'

class ProductDocumentSerializer(DocumentSerializer):

    class Meta:
        document = DocumentProduct
        fields = ('title', 'slug', 'color')

class CategoryProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'parent')