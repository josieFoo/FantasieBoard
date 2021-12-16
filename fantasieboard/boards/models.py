""" Model Definitionen für Boards """
from django.db import models


class Community(models.Model):
	"""
	Diese Klasse beinhaltet die Tabelle der Namen von Communities.
	Keine redundanten Namen erlaubt. (.pk) implizit erstellt.
	"""

	community_name = models.CharField(blank=False, max_length=32, unique=True)
	
	def __str__(self):
		return str(self.community_name)

class Users(models.Model):
	"""
 	Diese Klasse beinhaltet die Liste von Usern.
	Der Username ist einzigartig. 
	TODO: password sollte gehasht werden oder gar nicht angezeigt werden.
  	"""
	
	superuser = models.BooleanField(null=False, default=False)
	pseudo_name = models.CharField(blank=False, max_length=16, unique=True)
	created_on = models.DateField(auto_now_add=True)
	mail_address = models.EmailField(max_length=254, blank=False)
	password = models.CharField(blank=False, max_length=128) 

	def __str__(self):
		return str(self.pseudo_name)

class Community_moderator(models.Model):
	"""
	'Community_moderator' referenziert 'Users' und 'Community'.
	Zeigt welcher User welche Community moderiert.
	"""

	community_id = models.ForeignKey("Community", on_delete=models.CASCADE)
	admin_id = models.ForeignKey("Users", on_delete=models.CASCADE)
	
	def __str__(self) -> str:
		return f"{str(self.admin_id)}, {str(self.community_id)}"
 
class Articles(models.Model):
	"""
	Beinhaltet die Metadaten über die Beiträge sowie wer, wann, wo geschrieben hat etc.
	Jeder Beitrag hat 'community_id' und 'article_num' und somit primary key gebildet.
	Wenn 'pinned=True' dann, wird der Beitrag auf der obererste Zeile gepinnt.
	TODO: Entweder 'community_id' + 'article_num' als pk oder 
 	'global_article_id'als pk soll her.
	"""
	
	community_id = models.ForeignKey("Community", on_delete=models.CASCADE)
	title = models.CharField(blank=False, max_length=128)
	author_id = models.ForeignKey("Users", on_delete=models.CASCADE)
	pinned = models.BooleanField(null=False, default=False)
	written_on = models.DateField(auto_now=True)
	rich_txt = models.TextField(max_length=400, blank=False, default=" ")
	
	def __str__(self) -> str:
		return str(self.community_id) + str(self.pk)

class Comments(models.Model):
	"""
	Model für Kommentare.
	Ein Kommentar hat einen Autor und den darauf beziehenden Beitrag.
	"""
	
	article_id = models.ForeignKey("Articles", on_delete=models.CASCADE)
	user_id = models.ForeignKey("Users", on_delete=models.CASCADE)
	written_on = models.DateField(auto_now=True)
	rich_txt = models.TextField(max_length=100, blank=False, default=" ")
	
	def __str__(self):
		return str(self.pk) + str(self.article_id)

 
class Likes(models.Model):
	#community_id = models.ForeignKey("Community", on_delete=models.CASCADE)
	#article_num = models.ForeignKey("Articles", on_delete=models.CASCADE)
	article_id = models.ForeignKey("Articles", on_delete=models.CASCADE)
	user_id = models.ForeignKey("Users", on_delete=models.CASCADE) 