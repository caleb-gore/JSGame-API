from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    name = models.CharField(max_length=55)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    character_asset = models.ForeignKey("Asset", on_delete=models.CASCADE, related_name="character_asset", null=True, blank=True)
    enemy_asset = models.ForeignKey("Asset", on_delete=models.CASCADE, related_name="enemy_asset", null=True, blank=True)
    background_asset = models.ForeignKey("Asset", on_delete=models.CASCADE, related_name="background_asset", null=True, blank=True)
    trophy_asset = models.ForeignKey("Asset", on_delete=models.CASCADE, related_name="trophy_asset", null=True, blank=True)
    collectable_asset = models.ForeignKey("Asset", on_delete=models.CASCADE, related_name="collectable_asset", null=True, blank=True)
    other_asset = models.ForeignKey("Asset", on_delete=models.CASCADE, related_name="other_asset", null=True, blank=True)
    access_code = models.CharField(max_length=7, null=True, blank=True)
    
