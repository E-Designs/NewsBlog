# Generated by Django 3.2.7 on 2021-11-27 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_alter_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(default='post_default.jpg', upload_to='post_pics/'),
        ),
    ]
