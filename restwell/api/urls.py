from django.urls import path
from .views import UserView
from .views import UserDetailView
from .views import OrderView
from .views import OrderDetailView
from .views import CartItem

urlpatterns = [
    path('users', UserView.as_view(), name='users'),
    path('users/<uuid:user_id>', UserDetailView.as_view(), name='user_detail'),
    path('orders', OrderView.as_view(), name='orders'),
    path('cart-items', CartItemview.as_view(), name='cart-items'),
]