from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Customers


class CustomerRegistrationForm(UserCreationForm):

    username = forms.CharField()
    email = forms.EmailField()
    phone = forms.IntegerField()
    date_birth = forms.DateField()

    class Meta:
        model = Customers
        fields = ('username', 'email', 'phone', 'date_birth')
