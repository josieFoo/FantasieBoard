""" Model Definitionen für Boards """
from __future__ import annotations
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

#class Users(models.Model):
#	"""
# 	Diese Klasse ist obsolet. Wir ziehen um:
#	'from django.contrib.auth.models import User'
#  	"""
#	
#	superuser = models.BooleanField(null=False, default=False)
#	pseudo_name = models.CharField(blank=False, max_length=16, unique=True)
#	created_on = models.DateField(auto_now_add=True)
#	mail_address = models.EmailField(max_length=254, blank=False)
#	password = models.CharField(blank=False, max_length=128) 
#
#	def __str__(self):
#		return str(self.pseudo_name)
#
#	def createCommunity(self, name: str, moderators: list):
#		"""
#		0. ist der User superuser?
#		1. sollte überprüft werden, ob eine Community mit dem gleichen Namen existiert
#		2. wer die Moderatoren sind.
#  		"""
#		if self.superuser:
#			if not Community.objects.filter(community_name = name).exists():
#				new_community = Community.objects.create(community_name = name)
#				for mod in moderators:
#					new_community.add_moderator(mod)
#				return new_community
#		return 
#
#class User:
#	"""
#	default attributes
#	"""
#	id
#	last_login
#	is_superuser
#	username
#	first_name
#	last_name
#	email
#	is_staff
#	is_active
#	date_joined
#	https://docs.djangoproject.com/en/4.0/ref/contrib/auth/#django.contrib.auth.models.User

class Community(models.Model):
	"""
	Diese Klasse beinhaltet die Tabelle der Namen von Communities.
	Keine redundanten Namen erlaubt. (.pk) implizit erstellt.
	"""

	community_name = models.CharField(blank=False, max_length=32, unique=True)	
 
	def __str__(self):
		return str(self.community_name)
	
	def add_moderator(self, user: User):
		return Community_moderator.objects.create(
			   community_id = self, admin_id = user)
	def get_absolute_url(self):
		# Grammatik (schei...) Ich fasse ein Objekt nicht str!
		return reverse('community_detail', 
				 kwargs={"community_name": self.community_name,
						 })
	
class CommunityManager():
	...
 
 
class UsersManager():
	...
 

class Community_moderator(models.Model):
	"""
	'Community_moderator' referenziert 'User' und 'Community'.
	Zeigt welcher User welche Community moderiert.
	TODO: Mehrere Moderatoren für eine Community sollte möglich sein.
	"""

	community_id = models.ForeignKey("Community", on_delete=models.CASCADE)
	admin_id = models.ForeignKey(User, on_delete=models.CASCADE)
	
	def __str__(self) -> str:
		return f"{str(self.admin_id)}_{str(self.community_id)}"

	class Meta:
		"""
		Verhindert die Redundanz
		"""
		unique_together = (('community_id', 'admin_id'),)

class ModeratorManager():
	...


class Articles(models.Model):
	"""
	Beinhaltet die Daten über die Beiträge sowie wer, wann, wo geschrieben hat etc.
	Jeder Beitrag hat 'community_id' und primary key.
	TODO: Wenn 'pinned=True' dann, wird der Beitrag auf der obererste Zeile gepinnt.
	"""
	
	community_id = models.ForeignKey("Community", on_delete=models.CASCADE)
	title = models.CharField(blank=False, max_length=128)
	author_id = models.ForeignKey(User, on_delete=models.CASCADE)
	pinned = models.BooleanField(null=False, default=False)
	written_on = models.DateTimeField(auto_now=True)
	rich_txt = models.TextField(max_length=400, blank=False, default=" ")
	deleted = models.BooleanField(null=False, default=False)
	deleted_on = models.DateTimeField(default=timezone.now)

	def delete_on(self):
		self.deleted = True
		self.deleted_on = timezone.now()

	def get_absolute_url(self):
		
		return reverse('article_detail', 
					   kwargs={
					   "community_name": self.community_id.community_name,
					   "article_pk": self.pk
					          }
					   )

	def __str__(self) -> str:
		#return f"{str(self.community_id)}_{str(self.title)}"
		return str(self.title)

class Comments(models.Model):
	"""
	Model für Kommentare.
	Ein Kommentar hat einen Autor und den darauf beziehenden Beitrag.
	"""
	
	#pk = 'id'
	article_id = models.ForeignKey("Articles", on_delete=models.CASCADE) 
	user_id = models.ForeignKey(User, on_delete=models.CASCADE)
	written_on = models.DateTimeField(auto_now=True)
	rich_txt = models.TextField(max_length=100, blank=False, default=" ")
	
	def __str__(self):
		# return f"{str(self.pk)}_{str(self.article_id)}"
		return str(self.article_id)

class Likes(models.Model):
	"""
	Model für Likes-Zähler.
	TODO: Je ein User für je ein Article ein Like erlaubt. 
		  Redundante Likes verhindern. Jedes Like hat ein unique-ID.
	"""

	# pk='id'
	article_id = models.ForeignKey("Articles", on_delete=models.CASCADE)
	user_id = models.ForeignKey(User, on_delete=models.CASCADE)

	class Meta:
		unique_together = (('article_id', 'user_id'),)

	def __str__(self):
		return f"{str(self.user_id)} likes {str(self.article_id)}"


class LikesManager():
	...
 

"""Ende"""