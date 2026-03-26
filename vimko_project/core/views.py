from rest_framework import generics, status
from rest_framework.response import Response
from django.db import transaction
from .models import Product, Inventory, Dealer, Order, OrderItem
from .serializers import ProductSerializer, InventorySerializer, DealerSerializer, OrderSerializer
from rest_framework.permissions import IsAdminUser

# Products
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# Dealers
class DealerListCreateView(generics.ListCreateAPIView):
    queryset = Dealer.objects.all()
    serializer_class = DealerSerializer

class DealerRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Dealer.objects.all()
    serializer_class = DealerSerializer

# Inventory
class InventoryListView(generics.ListAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    
# Inventory Create
class InventoryCreateView(generics.CreateAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer    

# class InventoryUpdateView(generics.UpdateAPIView):
#     queryset = Inventory.objects.all()
#     serializer_class = InventorySerializer
#     lookup_field = 'product_id'
class InventoryUpdateView(generics.UpdateAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    lookup_field = 'product_id'

    permission_classes = [IsAdminUser]  # 🔥 Only admin can update

    def get_object(self):
        product_id = self.kwargs['product_id']
        return Inventory.objects.get(product_id=product_id)

# Orders
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

# Confirm Order
class OrderConfirmView(generics.GenericAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @transaction.atomic
    def post(self, request, pk):
        order = self.get_object()
        if order.status != 'Draft':
            return Response({"error": "Only draft orders can be confirmed."}, status=400)
        insufficient = []
        for item in order.items.all():
            if item.product.inventory.quantity < item.quantity:
                insufficient.append({
                    "product": item.product.name,
                    "available": item.product.inventory.quantity,
                    "requested": item.quantity
                })
        if insufficient:
            return Response({"error": "Insufficient stock", "details": insufficient}, status=400)
        # Deduct stock
        for item in order.items.all():
            item.product.inventory.quantity -= item.quantity
            item.product.inventory.save()
        order.status = 'Confirmed'
        order.save()
        return Response({"message": "Order confirmed successfully."})

# Deliver Order
class OrderDeliverView(generics.GenericAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def post(self, request, pk):
        order = self.get_object()
        if order.status != 'Confirmed':
            return Response({"error": "Only confirmed orders can be delivered."}, status=400)
        order.status = 'Delivered'
        order.save()
        return Response({"message": "Order delivered successfully."})