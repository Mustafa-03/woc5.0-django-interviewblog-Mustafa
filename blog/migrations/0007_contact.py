# Generated by Django 4.1.4 on 2023-01-20 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_alter_blog_author_alter_blog_rate'),
    ]

    operations = [
        migrations.CreateModel(
            name='contact',
            fields=[
                ('sno', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=50)),
                ('query', models.CharField(max_length=1000)),
            ],
        ),
    ]
