from django.db import models

# Create your models here.
class news(models.Model):
   topic = models.CharField(max_length=256)
   url = models.CharField(max_length=512)
   publisher = models.ForeignKey('publisher.publisher')
   description = models.TextField()
   pub_time = models.DateTimeField()
   f_cutted = models.PositiveSmallIntegerField(default=0)
