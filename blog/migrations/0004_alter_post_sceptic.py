# Generated by Django 3.2.7 on 2022-03-21 01:08

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0003_auto_20220320_1752'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='sceptic',
            field=models.ManyToManyField(blank=True, related_name='post_sceptic', to=settings.AUTH_USER_MODEL),
        ),
    ]
