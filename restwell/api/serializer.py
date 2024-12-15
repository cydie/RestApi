from rest_framework import serializers
from .models import User, Order, CartItem

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    
    class Meta:
        model = Order
        fields = '__all__'

    def validate(self, attrs):
        order_instance = Order(**attrs)
        order_instance.clean()
        return attrs

class CartItemSerializer(serializers.ModelSerializer):
    order = serializers.StringRelatedField()
    
    class Meta:
        model = CartItem
        fields = '__all__'
