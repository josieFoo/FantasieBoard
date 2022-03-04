from django.core.management.base import BaseCommand

class Command(BaseCommand):
	
	help = "article filter"
	
	def handle(self, *args, **options):
		 #queryset filtern nach delete status
		print("articles filtern möchte ich!")