# Generated by Django 4.1.4 on 2023-01-28 21:15

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0022_alter_profile_dob_blogcomments'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='BlogComments',
            new_name='BlogComment',
        ),
    ]
