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

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user)

    @action(detail=True, methods=['post'])
    def process_order(self, request, pk=None):
        order = self.get_object()
        if order.status == 'Pending':
            order.status = 'Processed'
            order.save()
            return Response({"detail": "Order processed successfully."})
        return Response({"detail": "Order is not pending."}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def cancel_order(self, request, pk=None):
        order = self.get_object()
        if order.status == 'Pending':
            order.status = 'Cancelled'
            order.save()
            return Response({"detail": "Order cancelled successfully."})
        return Response({"detail": "Order is already processed or cancelled."}, status=status.HTTP_400_BAD_REQUEST)

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
