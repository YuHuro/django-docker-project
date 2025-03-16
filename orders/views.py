from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import CartItem, Order, OrderItem
from .forms import OrderForm, OrderStatusForm
from menu.models import Dish

@login_required
def cart_detail(request):
    cart_items = CartItem.objects.filter(user=request.user)
    print(f"Контекст шаблона: {list(cart_items)}")
    total_price = sum(item.dish.actual_price * item.quantity for item in cart_items)
    return render(request, 'orders/cart_detail.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def update_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
    action = request.POST.get('action')

    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease' and cart_item.quantity > 1:
        cart_item.quantity -= 1
    cart_item.save()

    return redirect('cart_detail')

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
    cart_item.delete()
    return redirect('cart_detail')

@login_required
def clear_cart(request):
    CartItem.objects.filter(user=request.user).delete()
    return redirect('cart_detail')

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if not request.user.is_staff and request.user != order.user:
        return redirect('orders_list')

    form = None
    if request.user.is_staff:
        if request.method == "POST":
            form = OrderStatusForm(request.POST, instance=order)
            if form.is_valid():
                form.save()
                return redirect('order_detail', order_id=order.id)
        else:
            form = OrderStatusForm(instance=order)

    return render(request, 'orders/order_detail.html', {'order': order, 'form': form})

@login_required
def order_create(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items:
        return redirect('menu')
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.price = sum(item.total_price for item in cart_items)
            order.actual_price = order.price
            order.save()

            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    dish = cart_item.dish,
                    dish_name = cart_item.dish.short_name,
                    dish_price = cart_item.dish.actual_price,
                    quantity = cart_item.quantity
                )
        cart_items.delete()

        return  redirect('order_detail', order_id=order.id)

    else:
        form = OrderForm()

    return render(request, 'orders/order_create.html', {'form': form})

@login_required
def orders_list(request):
    if request.user.is_staff:
        orders = Order.objects.all()
    else:
        orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_list.html', {'orders': orders})

