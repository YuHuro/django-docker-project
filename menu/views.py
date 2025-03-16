from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import DishCategory, Dish
from orders.models import CartItem

def menu_view(request):
    categories = DishCategory.objects.prefetch_related('dishes').all()
    return render(request, 'menu/menu.html', {'categories': categories})

def add_to_cart(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, dish=dish)

    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('menu')
