from django.db import models

# Create your models here.
class publisher(models.Model):
    name = models.CharField(max_length=256)