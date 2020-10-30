from django import forms

from django.contrib.auth.forms import ReadOnlyPasswordHashField

from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from django.contrib import admin
from .models import Users, Stars, Customers, Categories, Orders, Avatars, Videos, CatPhoto


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Stars
        fields = ('email', 'username', 'password', 'first_name', 'last_name', 'phone', 'avatar',
                  'cat_name_id', 'price', 'rating', 'profession', 'description', 'tags',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Stars
        fields = ('email', 'username', 'password', 'first_name', 'last_name', 'phone', 'avatar',
                  'cat_name_id', 'price', 'rating', 'profession' ,'video_hi', 'description', 'tags',)

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]



@admin.register(Stars)
class StarsAdmin(BaseUserAdmin):
    """
    Админка для CRUD звезд
    """
    form = UserChangeForm
    add_form = UserCreationForm

    list_filter = ('rating', 'cat_name_id')
    fieldsets = (
        ('Инфорамция о Звезде',{
            'fields': (('email', 'username',), ('first_name', 'last_name'), 'phone', 'avatar', 'password')
        }),
        ('Коммерческая информация', {
            'fields': (('cat_name_id', 'price', 'rating',),'profession' ,'video_hi', ('description',),)
        }),
        ('Теги звезды', {
            'fields': ('tags', )
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'phone', 'username', 'price',
                       'rating', 'profession', 'cat_name_id')}
        ),
    )
    list_display = ('email', 'username', 'first_name', 'last_name')
    search_fields = ('email', 'first_name', 'last_name', 'username')
    ordering = ('email',)
    filter_horizontal = ()


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

admin.site.register(Avatars)
admin.site.register(Videos)
admin.site.register(CatPhoto)
# admin.site.register(TestAdmin)
