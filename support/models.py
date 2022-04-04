from django.utils import timezone
from django.db import models

# Create your models here.
class Issue(models.Model):
    user = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    subject = models.CharField(max_length=100)
    today = models.DateTimeField(default=timezone.now)
    discription = models.CharField(max_length=1000)