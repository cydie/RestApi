from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import User, Order, CartItem
from .serializer import UserSerializer, OrderSerializer, CartItemSerializer 


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=['get'])
    def pending_order(self, request, pk=None):
        user = self.get_object()
        if user.pending_order:
            serializer = OrderSerializer(user.pending_order)
            return Response(serializer.data)
        return Response({"detail": "No pending order."}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'])
    def orders(self, request, pk=None):
        user = self.get_object()
        orders = user.orders.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

class OrderViewSet(viewsets.ModelViewSet):
   
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    

    @action(detail=True, methods=['post'])
    def checkout(self, request, pk=None):
        try:
            order = self.get_object()
            if order.status != 'Pending':
                return Response({"error": "Only pending orders can be checked out."}, status=status.HTTP_400_BAD_REQUEST)
            
            cart_items = order.cart_items.all()
            if not cart_items.exists():
                return Response({"error": "No cart items found for this order."}, status=status.HTTP_400_BAD_REQUEST)


            order.status = 'Processed'
            order.save()
            return Response({"message": "Order successfully checked out."}, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def get_queryset(self):
        order_id = self.request.query_params.get('order')
        if order_id:
            return CartItem.objects.filter(order_id=order_id)
        return super().get_queryset()

    def create(self, request, *args, **kwargs):
        order_id = request.data.get('order')
        try:
            order = Order.objects.get(id=order_id, status='Pending')
        except Order.DoesNotExist:
            return Response({"detail": "Pending order not found."}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def pending_cart_items(self, request):
        order_id = request.query_params.get('order')
        if not order_id:
            return Response({"detail": "Order ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            order = Order.objects.get(id=order_id, status='Pending')
        except Order.DoesNotExist:
            return Response({"detail": "Pending order not found."}, status=status.HTTP_404_NOT_FOUND)
        cart_items = order.cart_items.all()
        serializer = self.get_serializer(cart_items, many=True)
        return Response(serializer.data)


class OrderListView(APIView):
    permission_classes = [IsAuthenticated]
    
    
    def get(self, request):
        order = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        data = request.data
        data['user'] = request.user.id 
        serializer = OrderSerializer(data=data)
        
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)