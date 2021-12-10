from django.db import models

# Create your models here.
class Community(models.Model):
	# id = models.AutoField(primary_key=True) -> Community.pk
	# die internen pks benutzen.
	community_name = models.CharField(blank=False, max_length=32, unique=True)

class Users(models.Model):
	# die internen pks benutzen.
	superuser = models.BooleanField(null=False, default=False)
	pseudo_name = models.CharField(blank=False, max_length=16, unique=True)
	created_at = models.DateField(auto_now_add=True)
	mail_address = models.EmailField(max_length=254, blank=False)
	password = models.CharField(blank=False, max_length=16)
 
class Community_moderator(models.Model):
	community_id = models.ForeignKey("Community", on_delete=models.CASCADE)
	admin_id = models.ForeignKey("Users", on_delete=models.CASCADE)
	#nochmal testen, ob mit foreign key funktioniert.
 
class Articles(models.Model):
	community_id = models.ForeignKey("Community", on_delete=models.CASCADE)
	#article_id = models.AutoField(primary_key=True) -> .pk
	article_num = models.IntegerField(unique=True)
	title = models.CharField(blank=False, max_length=128)
	author_id = models.ForeignKey("Users", on_delete=models.CASCADE)
	pinned = models.BooleanField(null=False, default=False)
	written_on = models.DateField(auto_now=True)
	rich_txt = models.TextField(max_length=400, blank=False, default=" ")
 
class Comments(models.Model):
	#community_id = models.ForeignKey("Community", on_delete=models.CASCADE)
	#comment_id = models.BigAutoField(unique=True) -> Comments.pk
	article_id = models.ForeignKey("Articles", on_delete=models.CASCADE)
	user_id = models.ForeignKey("Users", on_delete=models.CASCADE)
	written_on = models.DateField(auto_now=True)
	rich_txt = models.TextField(max_length=100, blank=False, default=" ")
 
class Likes(models.Model):
	#community_id = models.ForeignKey("Community", on_delete=models.CASCADE)
	#article_num = models.ForeignKey("Articles", on_delete=models.CASCADE)
	article_id = models.ForeignKey("Articles", on_delete=models.CASCADE)
	user_id = models.ForeignKey("Users", on_delete=models.CASCADE)

"""
 class Comment(models.Model):
	article = models.ForeignKey("Articles")

omment_obj = Comment()
article_obj = Article()

comment_obj.article = article_obj
comment_obj.article_id = article_obj.pk
# Beides geht!
 
 """
 