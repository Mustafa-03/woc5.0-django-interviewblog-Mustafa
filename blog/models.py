from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser,User
from autoslug import AutoSlugField
from datetime import date, datetime
from django.utils.timezone import now
from ckeditor.fields import RichTextField



class Blog(models.Model):
    id=models.BigAutoField(primary_key=True)
    company_name=models.CharField(max_length=100)
    job_profile=models.CharField(max_length=100)
    work_ex=models.IntegerField()
    offer_type=models.CharField(max_length=50)
    experience=RichTextField(blank=True,null=True)
    slug = AutoSlugField(populate_from='company_name',unique=True,default=None)
    rate=models.IntegerField(validators=[MaxValueValidator(10),MinValueValidator(0)], null=True)
    author=models.CharField(max_length=50, null=True)
    favourites=models.ManyToManyField(User, default=None, blank=True)
    updated_at=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.company_name


class contact(models.Model):
    sno=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    username=models.CharField(max_length=50)
    query=models.CharField(max_length=1000)


class Profile(models.Model):
    id=models.AutoField(primary_key=True)
    profile_user=models.OneToOneField(User,on_delete=models.CASCADE)
    fname=models.CharField(max_length=100)
    lname=models.CharField(max_length=100)
    degree=models.CharField(max_length=100)
    college=models.CharField(max_length=200)
    gender=models.CharField(max_length=50)
    dob=models.DateField()
    phone=models.CharField(max_length=10)
    email=models.EmailField()
    insta_handle=models.CharField(max_length=200,null=True)
    fb_handle=models.CharField(max_length=200,null=True)
    twitter_handle=models.CharField(max_length=200,null=True)
    forget_pass_token=models.CharField(max_length=100,null=True)
    profile_pic = models.ImageField(upload_to='profiles/',null=True)
    currwork = models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.profile_user

class BlogComment(models.Model):
    sno=models.AutoField(primary_key=True)
    comment=models.TextField()
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(Blog,on_delete=models.CASCADE)
    parent=models.OneToOneField('self', on_delete=models.CASCADE, null=True)
    timestamp=models.DateTimeField(default=now)

    def __str__(self):
        return self.comment[0:13] + "..." + " by " + self.user.username