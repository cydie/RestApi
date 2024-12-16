# api/urls.py
from django.urls import path
from .views import UserViewSet, OrderViewSet, CartItemViewSet

urlpatterns = [
    path('user/', UserViewSet.as_view({'get': 'list', 'post': 'create'}), name='user-list'),
    path('orders/', OrderViewSet.as_view({'get': 'list', 'post': 'create'}), name='order-list'),
    path('cart-items/', CartItemViewSet.as_view({'get': 'list', 'post': 'create'}), name='cartitem-list'),
]
