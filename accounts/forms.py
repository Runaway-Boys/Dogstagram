from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import DogAccount

class SignupForm(UserCreationForm):
    

    class Meta:
        model = DogAccount
        fields = '__all__'