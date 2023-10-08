from django.db import models

# Create your models here.

class MultipleImage(models.Model):
    images = models.CharField(max_length=512)
    name = models.CharField(max_length=64)
    
