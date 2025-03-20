from django.urls import path
from .views import menu_view, add_to_cart

urlpatterns = [
    path('', menu_view, name='menu'),
    path('add-to-cart/<int:dish_id>/', add_to_cart, name='add_to_cart'),
]