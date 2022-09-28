from django.db import models

class Asset(models.Model):
    name = models.CharField(max_length=55)
    width = models.IntegerField()
    height = models.IntegerField()
    frames = models.IntegerField()
    file = models.ImageField(
        upload_to='assets', height_field=None, width_field=None, max_length=None, null=True
    )
    type = models.CharField(max_length=55)