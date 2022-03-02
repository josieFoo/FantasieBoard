from django.contrib import admin

# Register your models here.
from .models import Community, Community_moderator, Articles, Comments, Likes

class ArticlesAdmin(admin.ModelAdmin):
	list_display = ('author_id', 'community_id', 'title', 'written_on')
	list_filter = ('pinned',)
	search_fields = ['author_id', 'community_id', 'title']
 
class CommunityAdmin(admin.ModelAdmin):
	list_display = ('community_name',)
	list_filter = ()
	search_fields = ['community_name']
 
class CommentsAdmin(admin.ModelAdmin):
	list_display = ('article_id', 'user_id', 'written_on')
	list_filter = ()
	search_fields = ['article_id']

admin.site.register(Community, CommunityAdmin)
admin.site.register(Community_moderator)
admin.site.register(Articles, ArticlesAdmin)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(Likes)
