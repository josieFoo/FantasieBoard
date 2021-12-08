from django.contrib import admin

# Register your models here.
from .models import Community, Users, Community_moderator

admin.site.register(Community)
admin.site.register(Users)
admin.site.register(Community_moderator)