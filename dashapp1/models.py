from django.db import models


# Create your models here.
class Sale(models.Model):
    item = models.CharField(max_length=50)
    price = models.FloatField()
