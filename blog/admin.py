from django.contrib import admin
from .models import Blog
from .models import contact
from .models import Profile
from .models import BlogComment
# Register your models here.

admin.site.register(Blog)
admin.site.register(contact)
admin.site.register(Profile)
admin.site.register(BlogComment)