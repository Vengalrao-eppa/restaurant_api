from rest_framework import serializers
from apis.models import Order, OrderItem
import datetime
from django.db import transaction

class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = '__all__'
        extra_kwargs = {
            'order': {'read_only': True}
        }

    def validate_quantity(self, value):
        if value == 0:
            raise serializers.ValidationError('Quantity must be greater then 0')
        return value

class OrderSerializer(serializers.ModelSerializer):

    order_items = OrderItemSerializer(many = True)

    class Meta:
        model = Order
        fields = '__all__'

    def validate_table(self, value):
        today = datetime.date.today()
        get_day_table = Order.objects.filter(table_id = value.id, created_date__gte = today)
        if len(get_day_table) > 0:
            raise serializers.ValidationError('No more order on this table for today.')
        return value
    
    @transaction.atomic
    def create(self, validated_data):
        data = validated_data
        order = Order.objects.create(user = data.get('user'), table = data.get('table'))
        item_list = []
        items = data.get('order_items')
        for item in items:
            orderitem = OrderItem(products = item.get('products'), quantity = item.get('quantity'), order_id = order.id)
            item_list.append(orderitem)
        if item_list:
            OrderItem.objects.bulk_create(item_list)
        return order

