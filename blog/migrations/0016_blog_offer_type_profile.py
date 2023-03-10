# Generated by Django 4.1.4 on 2023-01-26 17:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0015_alter_blog_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='offer_type',
            field=models.CharField(default='Internship', max_length=50),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
