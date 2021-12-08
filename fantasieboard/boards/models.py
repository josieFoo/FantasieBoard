from django.db import models

# Create your models here.
class Community(models.Model):
	id = models.AutoField(primary_key=True)
	community_name = models.CharField(blank=False, max_length=32)

class Users(models.Model):
	user_id = models.AutoField(primary_key=True)
	superuser = models.BooleanField(null=False, default=False)
	pseudo_name = models.CharField(blank=False, max_length=16)
	created_at = models.DateField(auto_now_add=True)
	mail_address = models.EmailField(max_length=254, blank=False)
	password = models.CharField(blank=False, max_length=16)
 
#class Community_moderator(models.Model):
#	community_id = models.ForeignKey(Community, on_delete=models.CASCADE)
#	admin_id = models.ForeignKey(Users, on_delete=models.CASCADE)
#	
#class Articles(models.Model):
#	community_id = models.Foreignkey(Community, on_delete=models.CASCADE)
#	article_num = models.AutoField(primary_key=True)
#	title = models.CharField(blank=False, max_length=128)
#	author_id = models.Foreignkey(Users, on_delete=models.CASCADE)
#class Comments(models.Model):
#	...
#class Likes():
#	...