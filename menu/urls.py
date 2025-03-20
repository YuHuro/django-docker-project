from django.urls import path
from django.shortcuts import redirect
from .views import menu_view, add_to_cart

urlpatterns = [
    path('/menu/', lambda request: redirect('/menu/', permanent=True)),
    path('menu/', menu_view, name='menu'),
    path('add-to-cart/<int:dish_id>/', add_to_cart, name='add_to_cart'),
]