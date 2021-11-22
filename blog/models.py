from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from .utility import Visability_State

# Create your models here.

class Post(models.Model):
    Local = 'Lc'
    National = 'Nt'
    Regional  = 'Rg'
    World = 'Wr'
    Business = 'Bs'
    Technology = 'Tc'
    Entertainment = 'En'
    Health = 'Hl'
    Lifestyle ='Lf'
    Political = 'Pl'
    Crime = 'Cr'
    Mysteries = 'Ms'
    Lost = "Ls"
    Sports = 'Sp'
    Obituaries = 'Ob'

    catagory_choices = [(Local, "Local"), (National, 'National'), (Regional, 'Regional'), (World, 'World')  ]
    subject_Choices = [(Business, 'Business'), (Technology, 'Technology'), (Entertainment, 'Entertainment'), 
    (Health, 'Health'), (Lifestyle, 'Lifestyle'), (Political, 'Political'), (Crime, 'Crime'), (Mysteries, 'Mysteries'),
    (Lost, 'Lost & Found'), (Sports, 'Sports'), (Obituaries, 'Obituaries')]


    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    catagory = models.CharField(max_length=100, choices= catagory_choices)
    subject = models.CharField(max_length=100, choices= subject_Choices)
    text = models.TextField()
    visability = models.CharField(max_length=15, help_text= Visability_State.pending + ', ' +
    Visability_State.under_review + ', ' + Visability_State.approved + ', ' + Visability_State.hidden)
    create_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})