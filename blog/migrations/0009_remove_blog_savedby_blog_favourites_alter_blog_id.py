# Generated by Django 4.1.4 on 2023-01-21 14:28

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0008_blog_savedby'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='savedby',
        ),
        migrations.AddField(
            model_name='blog',
            name='favourites',
            field=models.ManyToManyField(blank=True, default=None, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='blog',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
