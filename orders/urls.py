from django.urls import path
from .views import *

urlpatterns = [
    path('cart/', cart_detail, name='cart_detail'),
    path('cart/update/<int:cart_item_id>/', update_cart, name='update_cart'),
    path('cart/remove/<int:cart_item_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/clear/', clear_cart, name='clear_cart'),
    path('order/create/', order_create, name='order_create'),
    path('order/<int:order_id>/', order_detail, name='order_detail'),
    path('orders/', orders_list, name='orders_list'),
]