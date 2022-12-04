from django.db import models

# Create your models here.


class Member(models.Model):
    name = models.CharField (max_length=200)
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=100)
    tel = models.CharField(max_length=10)
    address = models.TextField(max_length=500)
