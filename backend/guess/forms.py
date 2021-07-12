from django import forms
from .models import *


class CheckoutContactForm(forms.Form):
    number = forms.IntegerField(required=True)