from rest_framework import serializers
from .models import User
from .models import Order
from .models import CartItem


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '_all_'
        

class CartItemSerializer(serializers.ModelSerializer):
    models = CartItem
    fields = '_all_'