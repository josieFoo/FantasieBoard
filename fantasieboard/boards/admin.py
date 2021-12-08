from django.contrib import admin

# Register your models here.
from .models import Community, Users

admin.site.register(Community)
admin.site.register(Users)