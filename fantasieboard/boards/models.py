from django.db import models

# Create your models here.
class Community(models.Model):
	# id = models.AutoField(primary_key=True) -> Community.pk
	# man will die internen pks benutzen.
	community_name = models.CharField(blank=False, max_length=32, unique=True)

class Users(models.Model):
	# man will die internen pks benutzen.
	superuser = models.BooleanField(null=False, default=False)
	pseudo_name = models.CharField(blank=False, max_length=16, unique=True)
	created_at = models.DateField(auto_now_add=True)
	mail_address = models.EmailField(max_length=254, blank=False)
	password = models.CharField(blank=False, max_length=16)
 
class Community_moderator(models.Model):
	community_id = models.ForeignKey("Community", on_delete=models.CASCADE)
	admin_id = models.ForeignKey("Users", on_delete=models.CASCADE)
	#nochmal testen, ob mit foreign key funktioniert.
#class Articles(models.Model):
#	community_id = models.Foreignkey("Community", on_delete=models.CASCADE)
#	article_num = models.AutoField(primary_key=True)
#	title = models.CharField(blank=False, max_length=128)
#	author_id = models.Foreignkey(Users, on_delete=models.CASCADE)
#class Comments(models.Model):
#	...
#class Likes():
#	...