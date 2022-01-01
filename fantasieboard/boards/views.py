from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.contrib.auth.models import User

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
	
	h2 = community_name
	com_db_id = Community.objects.get(community_name = community_name).pk
	queryset = Articles.objects.filter(community_id = com_db_id)
	context = {
		"articles": queryset,
		"community_name": h2,
	}
	
	return render(request, "community_detail.html", context)

def article_view(request, article_pk, **kwargs):
	"""
	shows the contents of the article.
	TODO: comments, liker should be shown if exists.
	"""
	
	queryset =  Articles.objects.get(id = article_pk)
	# wir haben ein keyword argument x=y 
	# x ist das Feld, das wir zugreifen möchten.
	# das y ist die variable, die wir von url bekommen hier z.B. 1 
	queryset_comments = Comments.objects.filter(article_id = article_pk)
	queryset_likes = Likes.objects.filter(article_id = article_pk)
	comments_count = len(queryset_comments)
	likes_count = len(queryset_likes)
	context = {
		"contents": queryset, 
		"comments": queryset_comments,
		"comments_num" : comments_count, # nicht angezeigt. Eventuell weiterverwendung möglich.
		"likers": queryset_likes, # nicht angezeigt. Eventuell weiterverwendung möglich.
		"likes": likes_count,
	}
	
	return render(request, "article_detail.html", context)

def profile_view(request, username, **kwargs):
	"""
 	shows user information.
	TODO: Field for image which will be uploaded by user.
 	"""
	
	queryset_user = Users.objects.get(pseudo_name = username)
	queryset_article = Articles.objects.filter(author_id = queryset_user)
	queryset_comment = Comments.objects.filter(user_id = queryset_user)
	article_count = len(queryset_article)
	comment_count = len(queryset_comment)
	context = {
		"user_profile": queryset_user,
		"article_count": article_count,
		"comment_count": comment_count,
	}
	return render(request, "profile.html", context)