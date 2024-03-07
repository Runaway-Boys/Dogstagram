from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django import forms
# Create your models here.

def get_profile_image_filepath(self,filename):
    return f'profile_images/{self.pk}/{"profile_image.png"}'

def get_default_profile_image():
    return "images/default-dog-profile.png"


class DogAccount(AbstractBaseUser):
    email =  models.EmailField(verbose_name = "email", max_length=60,unique=True,blank= True)
    username = models.CharField(max_length=30,unique=True,null = True)
    bio = models.TextField(max_length=255,blank=True)
    profile_image = models.ImageField(max_length=255,upload_to=get_profile_image_filepath, default= get_default_profile_image)
    location = models.CharField(max_length=100, blank=True)
    
    
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    hide_email = models.BooleanField(default = True)

    USERNAME_FIELD = "email" 
    REQUIRED_FIELDS = ['username']



    def __str__(self):
        return self.username
    
    def get_profile_image(self):
        return str(self.profile_image)[str(self.profile_image).index(f'profile_images/{self.pk}/'):]

    def has_perm(self,perm,obj=None):
        return self.is_admin
    
    def has_module_perms(self,app_label):
        return True