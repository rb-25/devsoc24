from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name=models.CharField(max_length=254)
    username= models.CharField(max_length=254, unique=True)
    email=models.EmailField(max_length=254, unique=True)    
    password=models.CharField(max_length=255)
    wins=models.IntegerField(default=0)

