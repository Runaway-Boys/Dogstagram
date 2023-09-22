from django.db import models
from django.conf import settings
# Create your models here.

class DogAccount(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    def __str__(user):
        return user