from django.db import models
# Create your models here.


class VinNumber(models.Model):
    vinNumber = models.CharField(max_length=100, primary_key=True)
    VDAFile = models.FileField()


