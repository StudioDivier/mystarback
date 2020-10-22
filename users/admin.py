from django.contrib import admin
from .models import Stars, Customers, Categories, Orders


@admin.register(Stars)
class StarsAdmin(admin.ModelAdmin):
    """
    Админка для CRUD звезд
    """
    list_display = ('username', 'rating', 'cat_name_id')
    list_filter = ('rating', 'cat_name_id')
    fieldsets = (
        ('Инфорамция о Звезде',{
            'fields': ('username', ('first_name', 'last_name'))
        }),
        ('Коммерческая информация', {
            'fields': ('cat_name_id', 'price', 'rating')
        }),
        ('Теги звезды', {
            'fields': ('tags', )
        }),
    )


@admin.register(Customers)
class CustomersAdmin(admin.ModelAdmin):
    """
    Админка для CRUD заказчиков
    """
    list_display = ('email', 'username', 'date_of_birth')


@admin.register(Categories)
class CategoryAdmin(admin.ModelAdmin):
    """
    Админка для CRUD категорий
    """
    list_display = ('cat_name',)


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    """
    Админка для CRUD заказов
    """
    fieldsets = (
        ('Заказ', {
            'fields': ('customer_id', 'star_id', ('status_order',))
        }),
        ('Информация о заказе', {
            'fields': ('for_whom', 'comment')
        }),
        ('Подробности', {
            'fields': ('order_price', 'ordering_time')
        }),
    )
