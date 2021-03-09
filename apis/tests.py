from django.test import TestCase
from rest_framework.test import APIClient
from apis.models import Order
from django.urls import reverse
from rest_framework import status
import json
from rest_framework.authtoken.models import Token
from apis.models import Tables, Product, Company, Menu, Profile

class OrdersTest(TestCase):

    
    def setUp(self):
        self.client = APIClient()
        self.user = Profile.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
        self.token = Token.objects.create(user=self.user)
        self.company = Company.objects.create(name='Demo', owner=self.user)
        self.menu = Menu.objects.create(name='DemoMenu', company=self.company)
        self.Table1 =  Tables.objects.create(company=self.company, name="Table No 1")
        self.Table2 =  Tables.objects.create(company=self.company, name="Table No 2")
        self.product1 = Product.objects.create(name='Chicken', sku='1', price=100)
        self.product1.menu.add(self.menu)
        self.product2 = Product.objects.create(name='Mutton', sku='2', price=100)
        self.product3 = Product.objects.create(name='Soup', sku='3', price=100)

    # for unauthenticated users
    def test_without_token(self):

        order = {
            "table": 1,
            "order_items": [
                    {
                        "products": 1,
                        "quantity": 1 
                    }
                ]
            }
        response = self.client.post(
            reverse('orders'),
            data=json.dumps(order),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 401)

    # for authenticaed users users
    def test_with_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        order = {
            "table": 1,
            "order_items": [
                    {
                        "products": 1,
                        "quantity": 1 
                    }
                ]
            }
        response = self.client.post(
            reverse('orders'),
            data=json.dumps(order),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

    # place order
    def test_place_order(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        order = {
            "table": self.Table1.id,
            "order_items": [
                    {
                        "products": self.product1.sku,
                        "quantity": 1 
                    }
                ]
            }
        response = self.client.post(
            reverse('orders'),
            data=json.dumps(order),
            content_type='application/json'
        )
        self.assertEqual(response.data.get('success'), True)
        self.assertEqual(response.data.get('message'), 'Order is successfully placed')

    def test_place_order_on_same_table_twice(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        order = {
            "table": self.Table1.id,
            "order_items": [
                    {
                        "products": self.product1.sku,
                        "quantity": 1 
                    }
                ]
            }
        response = self.client.post(
            reverse('orders'),
            data=json.dumps(order),
            content_type='application/json'
        )

        response2 = self.client.post(
            reverse('orders'),
            data=json.dumps(order),
            content_type='application/json'
        )
        self.assertEqual(response2.data.get('success'), False)
        self.assertEqual(response2.data.get('message'), 'Errors found')
        tableError = response2.data.get('data').get('table')
        print(tableError[0])

