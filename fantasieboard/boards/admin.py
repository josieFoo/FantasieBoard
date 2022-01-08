from django.contrib import admin

# Register your models here.
from .models import Community, Community_moderator, Articles, Comments, Likes


admin.site.register(Community)
admin.site.register(Community_moderator)
admin.site.register(Articles)
admin.site.register(Comments)
admin.site.register(Likes)
