from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Blog(models.Model):
    company_name=models.CharField(max_length=100)
    job_profile=models.CharField(max_length=100)
    work_ex=models.IntegerField()
    experience=models.CharField(max_length=2000)
    slug = models.CharField(max_length=100)
    rate=models.IntegerField(validators=[MaxValueValidator(10),MinValueValidator(0)])


    def __str__(self):
        return self.company_name
    