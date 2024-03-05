from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import UserManager
from django import forms
# Create your models here.

User = get_user_model()
class DogAccount(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    password = forms.CharField(widget=forms.PasswordInput)
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='default-dog-profile.jpg')
    location = models.CharField(max_length=100, blank=True)
    def __str__(user):
        return user