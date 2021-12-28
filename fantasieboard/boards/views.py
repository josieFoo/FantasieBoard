from django.shortcuts import render
from django.http import HttpResponse
from .models import *


# Create your views here.
def home_view(request, *args, **kwargs):
	"""
	home controller.
	will be extended.
	"""
	
	return render(request, "index.html", {})

def community_view(request, *args, **kwargs):
	"""
	Shows a list of communities which can be joined by users.
	'community.html' extends 'index.html'.
	"""

	queryset = Community.objects.all()
	context = {
		"community_list": queryset,
	}
	return render(request, "community.html", context)

def community_article(request, community_name, **kwargs):
	"""
	shows the articles of the community.
	"""
	
	com_db_id = Community.objects.get(community_name = community_name).pk
	queryset = Articles.objects.filter(community_id = com_db_id)
	context = {
		"articles": queryset,
	}
	
	return render(request, "community_detail.html", context)

def article_view(request, article_pk, **kwargs):
	"""
	shows the contents of the article.
	TODO: comments, liker should be shown if exists.
	"""
	
	queryset =  Articles.objects.get(id = article_pk)
	# wir haben ein keyword argument x=y 
  	# x ist das Feld das wir zugreifen möchten.
 	# das y ist die variable die wir von url bekommen hier z.B. 1 
	context = {
		"contents": queryset, 
	}
 
	return render(request, "article_detail.html", context)
