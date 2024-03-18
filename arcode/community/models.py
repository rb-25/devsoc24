from django.db import models
from users.models import User


class Friend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend')
    objects = models.Manager()
    
class Code(models.Model):
    title = models.CharField(max_length=100)
    code = models.TextField()
    language = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    objects = models.Manager()

class Comment(models.Model):
    code = models.ForeignKey('Code', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class Like(models.Model):
    code = models.ForeignKey('Code', on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class Resource(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    link = models.URLField()
    date = models.DateTimeField(auto_now_add=True)
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    objects = models.Manager()

