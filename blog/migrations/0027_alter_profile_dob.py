# Generated by Django 4.1.4 on 2023-01-29 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0026_alter_blog_experience'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='dob',
            field=models.DateTimeField(),
        ),
    ]
