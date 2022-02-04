from urllib import request
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import context

# Create your views here.
from .models import *
from .forms import CommentForm, RegisterUserForm, ArticleForm

def home_view(request, *args, **kwargs):
	"""
	home controller.
	will be extended.
	"""

	if request.user.is_authenticated:
		return redirect('community')
	else:
		return render(request, "index.html", {})

def community_view(request, *args, **kwargs):
	"""
	Shows a list of communities which can be joined by users.
	'community.html' extends 'index.html'.
	"""
	
	queryset = Community.objects.all()
	anonymoususer = "a nameless Hero"
	context = {
		"community_list": queryset,
		"anonymoususer" : anonymoususer,
	}
	
	return render(request, "community.html", context)

def community_article(request, community_name, **kwargs):
	"""
	shows the articles of the community.
	"""

	h2 = community_name
	com_db_id = Community.objects.get(community_name = community_name).pk
	queryset = Articles.objects.filter(community_id = com_db_id).order_by("-written_on")
	context = {
		"articles": queryset,
		"community_name": h2,
	}

	return render(request, "community_detail.html", context)

def article_view(request, article_pk, **kwargs):
	"""
	shows the contents of the article and its
	comments and likes if exist.
	"""

	queryset =  Articles.objects.get(id = article_pk)
	article_id = article_pk
	community_id = queryset.community_id
	# wir haben ein keyword argument x=y
	# x ist das Feld, das wir zugreifen möchten.
	# das y ist die variable, die wir von url bekommen hier z.B. 1
	queryset_comments = Comments.objects.filter(article_id = article_pk).order_by("-written_on")
	queryset_likes = Likes.objects.filter(article_id = article_pk)
	comments_count = len(queryset_comments)
	likes_count = len(queryset_likes)
	context = {
		"contents": queryset,
		"comments": queryset_comments,
		"comments_num" : comments_count, # nicht angezeigt. Eventuell weiterverwendung möglich.
		"likers": queryset_likes, # nicht angezeigt. Eventuell weiterverwendung möglich.
		"likes": likes_count,
		"article_pk": article_id,
		"community_name": community_id,
	}

	return render(request, "article_detail.html", context)

@login_required(login_url='login')
def profile_view(request, username, **kwargs):
	"""
 	shows user information.
	TODO: Field for image which will be uploaded by user.
 	"""

	queryset_user = User.objects.get(username = username)
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

def register_view(request, *args, **kwargs):
	"""
	shows User Registration page.
	using Django default UserCreationForm.
	'/register/' calls 'views.register_view', 
 	and the view renders 'register.html'.
	If the form calls method 'POST', 
 	the form will be checked and saved.
	"""

	form = RegisterUserForm()
	if request.method == 'POST':
		form = RegisterUserForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			form.save()
			messages.success(
				request, "You have successfully registered, " + username + "."
		 	)
			return redirect('login')
	context = {
		"form": form,
	}

	return render(request, "register.html", context)

def login_view(request, *args, **kwargs):
	"""
	'/login' calls 'login_view'.
	'login_view' renders login page.
	The View gets username and password from the page.
	"""

	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('community')
		else:
			messages.info(request, "Username or Password is incorrect.")

	context = {}
	return render(request, "login.html", context)

@login_required(login_url='login')
def logout_view(request, *args, **kwargs):
	"""
	renders logout page.
	'logout/' calls 'logout_view'.
	Username need to be saved before logging out for 
	themessage on the logout page.
	"""

	username = request.user
	context = { 'username': username }
	logout(request)
	return render(request, "logout.html", context)

@login_required(login_url='login')
def write_article(request, community_name, **kwargs):
	"""
	renders article writing page.
	"""

	username = request.user
	community = Community.objects.get(community_name = community_name)
	# Es sollte ein Objekt sein.
	form = ArticleForm() 
	context={ 
			'form': form,
			}

	if request.method == 'POST':
		article = Articles.objects.create(community_id = community, author_id=username)
		article.save()
		form = ArticleForm(request.POST, instance=article)
		if form.is_valid():
			article_object = form.save()
			return redirect(article_object.get_absolute_url())

	return render(request, "write_article.html", context)

@login_required(login_url='login')
def edit_article(request, article_pk, **kwargs):
	"""
	rendert edit windows
	"""

	article = Articles.objects.get(id=article_pk)
	form = ArticleForm(instance=article)
	community = article.community_id
	
	if request.method == 'POST':
		form = ArticleForm(request.POST, instance=article)
		if form.is_valid():
			form.save()
			return redirect(article.get_absolute_url()) 

	context = { 'form':form, 'article':article, 'community':community }

	return render(request, 'write_article.html', context)

@login_required(login_url='login')
def delete_article(request, article_pk, **kwargs):
	""" 
 	assures whether the article should be deleted.
	On confirm the article will be deleted.
 	"""

	article = Articles.objects.get(id=article_pk)
	community = article.community_id

	if request.method == 'POST':
		article.delete()
		return redirect(community.get_absolute_url())

	context = {
    		'article': article, 
			'community_name': community,
			'article_pk': article_pk,
    }
	return render(request, 'delete_article.html', context)

@login_required(login_url='login')
def reply_article(request, article_pk, **kwargs):
	"""
	renders form for a comment.
	"""
	
	queryset =  Articles.objects.get(id = article_pk)
	article_id = article_pk
	community_id = queryset.community_id
	queryset_comments = Comments.objects.filter(article_id = article_pk).order_by("-written_on")
	queryset_likes = Likes.objects.filter(article_id = article_pk)
	comments_count = len(queryset_comments)
	likes_count = len(queryset_likes)

	form = CommentForm()
	context = {
     	"contents": queryset,
		"comments": queryset_comments,
		"comments_num" : comments_count, # nicht angezeigt. Eventuell weiterverwendung möglich.
		"likers": queryset_likes, # nicht angezeigt. Eventuell weiterverwendung möglich.
		"likes": likes_count,
		"article_pk": article_id,
		"community_name": community_id,
		"form": form,
	}

	if request.method == 'POST': # object not str!!!
		comment = Comments.objects.create(article_id=queryset, user_id=request.user)
		comment.save()
		form = CommentForm(request.POST, instance=comment)
		if form.is_valid():
			form.save()
			return redirect(queryset.get_absolute_url())
	return render(request, "reply.html", context)

@login_required(login_url='login')
def delete_comment(request, article_pk, comment_pk, **kwargs):
	"""
	delete comment
	"""

	article = Articles.objects.get(pk=article_pk)
	comments = Comments.objects.filter(article_id = article_pk).order_by("-written_on")
	comment = Comments.objects.get(pk=comment_pk)
	community_name = article.community_id

	context ={ 'article': article,
			   'comments': comments,
			   'community_name': community_name,
			   'article_pk': article.pk,
			   'comment': comment,
	}

	if request.method == 'POST':
		comment.delete()
		return redirect(article.get_absolute_url())

	return render(request, 'delete_comment.html', context)

@login_required(login_url='login')
def edit_comment(request, article_pk, comment_pk, **kwargs):
	""""
	edit comment
	"""
	
	queryset =  Articles.objects.get(id = article_pk)
	article_id = article_pk
	community_id = queryset.community_id
	queryset_comments = Comments.objects.filter(article_id = article_pk).order_by("-written_on")
	queryset_likes = Likes.objects.filter(article_id = article_pk)
	comments_count = len(queryset_comments)
	likes_count = len(queryset_likes)
	comment = Comments.objects.get(pk = comment_pk)

	form = CommentForm(instance=comment)
	
	if request.method == 'POST':
		form = CommentForm(request.POST, instance=comment)
		if form.is_valid():
			form.save()
			return redirect(queryset.get_absolute_url())

	context = {
		"contents": queryset,
		"comments": queryset_comments,
		"comments_num" : comments_count, # nicht angezeigt. Eventuell weiterverwendung möglich.
		"likers": queryset_likes, # nicht angezeigt. Eventuell weiterverwendung möglich.
		"likes": likes_count,
		"article_pk": article_id,
		"community_name": community_id,
		"form": form,
		"comment_pk":comment_pk
	}
	
	return render(request, 'reply.html', context)