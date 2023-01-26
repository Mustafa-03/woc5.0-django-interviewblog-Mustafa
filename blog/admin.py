from django.contrib import admin
from .models import Blog
from .models import contact
from .models import Profile
# Register your models here.

admin.site.register(Blog)
admin.site.register(contact)
admin.site.register(Profile)