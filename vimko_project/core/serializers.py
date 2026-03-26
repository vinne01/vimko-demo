from rest_framework import serializers
from .models import Product, Inventory, Dealer, Order, OrderItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class InventorySerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    class Meta:
        model = Inventory
        fields = ['id', 'product', 'product_name', 'quantity']

class DealerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dealer
        fields = '__all__'

# class OrderItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OrderItem
#         fields = ['id', 'product', 'quantity', 'unit_price', 'line_total']
class OrderItemSerializer(serializers.ModelSerializer):
    unit_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    line_total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'unit_price', 'line_total']
        
    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        return value     

# class OrderSerializer(serializers.ModelSerializer):
#     items = OrderItemSerializer(many=True)
#     class Meta:
#         model = Order
#         fields = ['id', 'dealer', 'order_number', 'status', 'total_amount', 'items']

#     def create(self, validated_data):
#         items_data = validated_data.pop('items')
#         order = Order.objects.create(**validated_data)
#         total_amount = 0
#         for item_data in items_data:
#             item = OrderItem.objects.create(order=order, **item_data)
#             total_amount += item.line_total
#         order.total_amount = total_amount
#         order.save()
#         return order

#     def update(self, instance, validated_data):
#         if instance.status != 'Draft':
#             raise serializers.ValidationError("Cannot edit non-draft order.")
#         items_data = validated_data.pop('items', [])
#         instance.dealer = validated_data.get('dealer', instance.dealer)
#         instance.save()
#         # Update order items
#         instance.items.all().delete()
#         total_amount = 0
#         for item_data in items_data:
#             item = OrderItem.objects.create(order=instance, **item_data)
#             total_amount += item.line_total
#         instance.total_amount = total_amount
#         instance.save()
#         return instance

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'dealer', 'order_number', 'status', 'total_amount', 'items']
        read_only_fields = ['order_number', 'status', 'total_amount']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        total_amount = 0

        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']
            unit_price = product.price
            line_total = unit_price * quantity

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                unit_price=unit_price,
                line_total=line_total
            )
            total_amount += line_total

        order.total_amount = total_amount
        order.save()
        return order

    def update(self, instance, validated_data):
        if instance.status != 'Draft':
            raise serializers.ValidationError("Cannot edit non-draft order.")

        items_data = validated_data.pop('items', [])
        instance.dealer = validated_data.get('dealer', instance.dealer)
        instance.save()

        instance.items.all().delete()
        total_amount = 0

        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']
            unit_price = product.price
            line_total = unit_price * quantity

            OrderItem.objects.create(
                order=instance,
                product=product,
                quantity=quantity,
                unit_price=unit_price,
                line_total=line_total
            )
            total_amount += line_total

        instance.total_amount = total_amount
        instance.save()
        return instance