# Generated by Django 4.1.4 on 2023-01-28 21:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0024_alter_blogcomment_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogcomment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.blog'),
        ),
    ]