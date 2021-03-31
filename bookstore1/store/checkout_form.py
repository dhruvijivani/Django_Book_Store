from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Order

class CheckForm(forms.ModelForm):
    state=forms.CharField(required=True)
    city=forms.CharField(required=True)
    pincode=forms.CharField(required=True)
    class Meta:
        model=Order
        fields = ['address' ,'state','city','pincode','phone' , 'payment_method']