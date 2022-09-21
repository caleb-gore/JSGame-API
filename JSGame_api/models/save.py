from django.db import models
from django.contrib.auth.models import User

class Save(models.Model):
    score = models.IntegerField()
    level = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_saved = models.DateTimeField(auto_now=True)
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    lives = models.IntegerField()
    game_over = models.BooleanField(default=False)
    awarded_trophies = models.ManyToManyField("Trophy", related_name="awarded_trophies", blank=True)