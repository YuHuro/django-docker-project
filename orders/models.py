from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from menu.models import Dish
from django.utils.timezone import now

class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('indelivery', 'В доставке'),
        ('delivered', 'Доставлен'),
    ]
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders", verbose_name="Пользователь")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    actual_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Текущая цена", null=True)
    address = models.CharField(max_length=255, verbose_name="Адрес")
    phone_number = models.CharField(max_length=15, verbose_name="Номер телефона", blank=True, null=True)
    order_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Статус заказа")
    created_at = models.DateTimeField(default=now, verbose_name="Дата создания")

    def __str__(self):
        return f"Заказ {self.id} - {self.user.username}"

class OrderAction(models.Model):
    ACTION_CHOICES = [
        ('to_delivery', 'Отправлено в доставку'),
        ('done', 'Завершено'),
    ]
    id = models.AutoField(primary_key=True)
    comment = models.TextField(verbose_name="Комментарий")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='actions', verbose_name="Заказ")
    manager_name = models.CharField(max_length=100, verbose_name="Менеджер")
    action = models.CharField(max_length=20, choices=ACTION_CHOICES, verbose_name="Действие")

    def __str__(self):
        return f"Действие {self.id} - {self.action} (Менеджер: {self.manager_name})"

class OrderItem(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items', verbose_name="Заказ")
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, verbose_name="Блюдо")  # Ссылка на оригинальное блюдо
    dish_name = models.CharField(max_length=100, verbose_name="Название блюда на момент заказа")
    dish_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена блюда на момент заказа")
    quantity = models.PositiveIntegerField(verbose_name="Количество")

    def __str__(self):
        return f"{self.dish_name} (x{self.quantity}) - {self.dish_price} руб."

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart_items", verbose_name="Пользователь")
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, verbose_name="Блюдо")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")

    def __str__(self):
        return f"{self.dish.short_name} x {self.quantity}"

    @property
    def total_price(self):
        return self.dish.actual_price * self.quantity