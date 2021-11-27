# Generated by Django 3.2.7 on 2021-11-07 00:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('location', models.CharField(max_length=100)),
                ('catagory', models.CharField(max_length=100)),
                ('subject', models.CharField(max_length=100)),
                ('text', models.TextField()),
                ('visability', models.CharField(choices=[('p', 'pending'), ('a', 'approved'), ('U', 'under-review'), ('h', 'hidden')], default='p', max_length=15)),
                ('create_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('published_date', models.DateField(blank=True, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]