from django.db import models
from django.contrib.auth.models import User

class Trophy(models.Model):
    type = models.CharField(max_length=55)
    asset = models.ForeignKey("Asset", on_delete=models.CASCADE)
    awarded_trophies = models.ManyToManyField(User)
