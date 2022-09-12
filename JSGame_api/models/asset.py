from django.db import models

class Asset(models.Model):
    name = models.CharField(max_length=55)
    width = models.IntegerField()
    height = models.IntegerField()
    file = models.ImageField()
    type = models.CharField(max_length=55)