from django.db import models

# Create your models here.


class Member(models.Model):
    name = models.CharField (max_length=200)
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=100)
    tel = models.CharField(max_length=10)
    address = models.TextField(max_length=500)

class Post(models.Model):
    post_by = models.CharField(max_length=50)
    post_date = models.DateTimeField(auto_now_add=True)
    post_text = models.TextField(max_length=500)