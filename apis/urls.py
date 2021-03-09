from django.urls import path
from rest_framework.authtoken import views
from apis.views import OrderView

urlpatterns = [
    path('login', views.obtain_auth_token, name="login"),
    path('place-order', OrderView.as_view(), name="orders")
]