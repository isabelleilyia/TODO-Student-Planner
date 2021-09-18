from django.contrib import admin

# Register your models here.
from .models import User, Project, Link, ToDo

admin.site.register(User)
admin.site.register(Project)
admin.site.register(Link)
admin.site.register(ToDo)