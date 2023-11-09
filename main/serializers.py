from rest_framework import serializers
from .models import CreateAdvertisementDetskiymir


class AdvertisementDetskiymirSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreateAdvertisementDetskiymir
        fields = '__all__'

