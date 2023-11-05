from rest_framework import serializers
from django.contrib.auth.views import get_user_model

from .models import SellMessages, BuyMessage

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')

class SellMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellMessages
        fields = '__all__'

class BuyMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyMessage
        fields = '__all__'