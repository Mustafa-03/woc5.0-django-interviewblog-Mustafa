from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser,User

class Blog(models.Model):
    company_name=models.CharField(max_length=100)
    job_profile=models.CharField(max_length=100)
    work_ex=models.IntegerField()
    experience=models.CharField(max_length=2000)
    slug = models.CharField(max_length=100)
    rate=models.IntegerField(validators=[MaxValueValidator(10),MinValueValidator(0)], null=True)
    author=models.CharField(max_length=50, null=True)
    savedby=models.CharField(max_length=100,null=True)


    def __str__(self):
        return self.company_name


class contact(models.Model):
    sno=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    username=models.CharField(max_length=50)
    query=models.CharField(max_length=1000)