from django.db import models

# Create your models here.
class Url(models.Model):
    url = models.CharField(max_length=200)
    frequency_list = models.TextField()
    