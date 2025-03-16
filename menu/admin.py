from django.contrib import admin
from django.utils.html import format_html
from .models import DishCategory, Dish

class DishInline(admin.TabularInline):
    model = Dish
    extra = 1
    fields = ('short_name', 'price', 'actual_price', 'image', 'image_preview')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px;"/>', obj.image.url)
        return ""
    image_preview.short_description = "Превью изображения"

class DishCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    inlines = [DishInline]

class DishAdmin(admin.ModelAdmin):
    list_display = ('short_name', 'category', 'price', 'actual_price', 'image_preview')
    list_filter = ('category',)
    search_fields = ('short_name', 'full_name',)
    readonly_fields = ('image_preview',)
    fields = ('short_name', 'full_name', 'price', 'actual_price', 'image', 'category', 'image_preview')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px;"/>', obj.image.url)
        return ""
    image_preview.short_description = "Превью изображения"

admin.site.register(DishCategory, DishCategoryAdmin)
admin.site.register(Dish, DishAdmin)

