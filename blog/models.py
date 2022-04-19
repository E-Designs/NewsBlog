import random
from re import U
from typing import Tuple
from django.conf import settings
from django.db import models
from django.db.models.fields import CharField
from django.db.models.signals import pre_save, post_save
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User
from .utility import Visability_State
from PIL import Image
from django.urls import reverse

# Create your models here.

class Post(models.Model):
    Local = 'Local'
    National = 'National'
    Regional  = 'Reginal'
    World = 'World'
    Business = 'Business'
    Technology = 'Technology'
    Entertainment = 'Entertainment'
    Health = 'Health'
    Lifestyle ='Lifestyle'
    Political = 'Political'
    Crime = 'Crime'
    Mysteries = 'Mysteries'
    Lost = "Lost"
    Sports = 'Sports'
    Obituaries = 'Obituaries'
    Announcements = 'Annoncements'


    region_choices = [(Local, "Local"), (National, 'National'), (Regional, 'Regional'), (World, 'World')  ]
    subject_choices = [(Business, 'Business'), (Technology, 'Technology'), (Entertainment, 'Entertainment'), 
    (Health, 'Health'), (Lifestyle, 'Lifestyle'), (Political, 'Political'), (Crime, 'Crime'), (Mysteries, 'Mysteries'),
    (Lost, 'Lost & Found'), (Sports, 'Sports'), (Obituaries, 'Obituaries'), (Announcements, 'Announcements'),]


    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(blank=True, null= True, unique=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100) 
    region = models.CharField(max_length=100, choices= sorted(region_choices))
    subject = models.CharField(max_length=100, choices= sorted(subject_choices))
    text = models.TextField()
    visability = models.CharField(max_length=15, help_text= Visability_State.pending + ', ' +
    Visability_State.under_review + ', ' + Visability_State.approved + ', ' + Visability_State.hidden)
    image = models.ImageField(upload_to='post_pics/', default='post_default.jpg')
    believer = models.ManyToManyField(User, related_name='post_believe', blank=True)
    sceptic = models.ManyToManyField(User, related_name='post_sceptic', blank=True)
    create_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return '%s - %s' % (self.author, self.title)

    @property
    def name(self):
        return self.title

    def number_of_believers(self):
        return self.believer.count()

    def number_of_sceptics(self):
        return self.sceptic.count()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 600 or img.width > 600:
            output_size =(600,600)
            img.thumbnail(output_size)
            img.save(self.image.path)


    def get_absolute_url(self):
        return reverse('post_detail' , kwargs={'pk': self.pk} )

def post_pre_save(sender, instance, *args, **kwargs):
     if instance.slug is None:
         slugify_instance_title(instance, save=False)

pre_save.connect(post_pre_save, sender=Post)

def slugify_instance_title(instance, save=False, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    qs = Post.objects.filter(slug=slug).exclude(id=instance.id)

    if qs.exists():
        rand_int = random.randint(1000, 9000)
        slug = f"{slug}-{rand_int}"
        return slugify_instance_title(instance, save=save, new_slug=slug)
    
    instance.slug = slug

    if save:
        instance.save()
    return instance
def post_post_save(sender, instance, created, *args, **kwargs):
    if created:
        slugify_instance_title(instance, save=True)

post_save.connect(post_post_save, sender=Post)

class Comment(models.Model):

    comment_author = models.ForeignKey(User, on_delete=models.CASCADE)
    story = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    create_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '%s - %s' % (self.story, self.text) 