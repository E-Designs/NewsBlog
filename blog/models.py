from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    visability_state = [('p','pending'), ('a', 'approved'), ( 'U', 'under-review'), ('h', 'hidden')]
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    catagory = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    text = models.TextField()
    visability = models.CharField(max_length=15,choices=visability_state, default='p')
    create_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})