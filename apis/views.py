from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication

# local imports
from apis.serailizers import OrderSerializer, OrderItemSerializer
from apis.models import Order, OrderItem

# Create your views here.

class OrderView(APIView):
    authentication_classes = [TokenAuthentication,]

    def post(self, request):
        dictV = {}
        data = request.data
        data.update({
            'user': request.user.id
        })
        serializer = OrderSerializer(data=data)
        if serializer.is_valid():
            order = serializer.save()
            dictV = {
                'success': True,
                'message': 'Order is successfully placed',
                'data': serializer.data
            }
        else:
            if serializer.errors:
                dictV = {
                    'success': False,
                    'message': 'Errors found',
                    'data': serializer.errors
                }
        return Response(dictV)

    
    def put(self, request):
        dictV = {}
        id = request.GET.get('id')
        try:
            order = Order.objects.get(id = id)
            data = request.data
            OrderItem.objects.filter(order = order.id).delete()
            items = [{**item, 'order': order} for item in data.get('order_items')]
            serializer = OrderItemSerializer(data=items, many=True)
            if serializer.is_valid():
                orderitems = [OrderItem(quantity = item.get('quantity'), order_id=id, products_id= item.get('products')) for item in serializer.data]
                OrderItem.objects.bulk_create(orderitems)
                dictV = {
                    'success': True,
                    'message': 'Order is successfully updated',
                    'data': serializer.data
                }
            else:
                if serializer.errors:
                    dictV = {
                        'success': False,
                        'message': 'Errors found',
                        'data': serializer.errors
                    }
        except Order.DoesNotExist:
            dictV = {
                    'success': False,
                    'message': 'Invalid Order id / Order id is required.',
                    'data': []
                }
        return Response(dictV)
