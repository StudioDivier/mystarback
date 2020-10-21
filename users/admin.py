from django.contrib import admin
from .models import Stars, Customers, Categories, Orders, ExtraCategories


class ExtraCatAdmin(admin.TabularInline):
    model = ExtraCategories


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
    )
    inlines = [
        ExtraCatAdmin
    ]


class CustomersAdmin(admin.ModelAdmin):
    """
    Админка для CRUD заказчиков
    """
    list_display = ('email', 'username', 'date_of_birth')


class CategoryAdmin(admin.ModelAdmin):
    """
    Админка для CRUD категорий
    """
    list_display = ('cat_name',)


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


admin.site.register(Categories, CategoryAdmin)
admin.site.register(Stars, StarsAdmin)
admin.site.register(Customers, CustomersAdmin)
admin.site.register(Orders, OrdersAdmin)
admin.site.register(ExtraCategories)

