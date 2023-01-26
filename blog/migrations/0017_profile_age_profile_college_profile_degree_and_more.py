# Generated by Django 4.1.4 on 2023-01-26 17:32

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0016_blog_offer_type_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='age',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='college',
            field=models.CharField(default='College', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='degree',
            field=models.CharField(default='Degree', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='dob',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='gender',
            field=models.CharField(default='Male', max_length=50),
            preserve_default=False,
        ),
    ]
