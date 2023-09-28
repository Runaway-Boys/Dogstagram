from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()
class DogAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    breed = models.CharField(max_length=50,blank=True,null=True)
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='default-dog-profile.jpg')
    location = models.CharField(max_length=100, blank=True)
    def __str__(user):
        return user