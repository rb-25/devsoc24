from django.db import models

class Snake(models.Model):
    name = models.CharField(max_length=100)
    score = models.IntegerField()

class Dino(models.Model):
    name = models.CharField(max_length=100)
    score = models.IntegerField()

class SnakeQuestion(models.Model):
    question = models.CharField(max_length=100)
    answer = models.CharField(max_length=100)
    no_of_lines = models.IntegerField()

class DinoQuestion(models.Model):
    question = models.CharField(max_length=100)
    answer = models.CharField(max_length=100)
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100)
