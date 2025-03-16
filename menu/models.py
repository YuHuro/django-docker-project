from django.db import models
from django.core.exceptions import ValidationError

class DishCategory(models.Model):
    name = models.CharField(max_length=25, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Dish(models.Model):
    id = models.AutoField(primary_key=True)
    short_name = models.CharField(max_length=50, verbose_name="Краткое название")
    full_name = models.TextField(verbose_name="Полное название")
    actual_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Текущая цена")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    image = models.ImageField(upload_to="dish/images/", null=True, blank=True, default="dish/images/default.jpg")
    category = models.ForeignKey(DishCategory, on_delete=models.CASCADE, related_name="dishes", verbose_name="Категория")

    def __str__(self):
        return self.short_name

    def __repr__(self):
        return 'Resume(%s, %s)' % (self.short_name, self.image)

    def clean(self):
        if self.price < 1.00:
            raise ValidationError('Цена не может быть меньше 1 доллара.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
