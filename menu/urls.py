from django.urls import path

from .views import menu_view, add_to_cart

app_name = 'menu'

urlpatterns = [
    path('menu/', menu_view, name='menu'),
    path('add-to-cart/<int:dish_id>/', add_to_cart, name='add_to_cart'),
]