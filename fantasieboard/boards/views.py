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
from .forms import CommentForm, RegisterUserForm 
from .forms import ArticleForm, ArticleUserForm

def community_not_found_404(request, *args, **kwargs):
	
	community_list = Community.objects.all()
	if not community_list.exists():
		return redirect('community')

	return redirect('community')

def home_view(request, *args, **kwargs):
	"""
	home controller.
	will be extended.
	"""
 
	community_list = Community.objects.all()
	context = { "community_list": community_list, }
	if request.user.is_authenticated:
		return redirect('community')
	else:
		return render(request, "index.html", context)

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

	community_list = Community.objects.all()
	h2 = community_name
	
	try:
		community_pk = Community.objects.get(community_name = community_name).pk
	except:
		return redirect('community')

	queryset = Articles.objects.filter(community_id = community_pk).order_by("-written_on")
	pinned_set = queryset.filter(pinned = True)
	unpinned_set = queryset.filter(pinned = False)

	pinned_comment_counter = []
	for query in pinned_set:
		article_pk = query.pk
		pinned_set_comments = Comments.objects.filter(article_id = article_pk).order_by("-written_on")
		comment_number = pinned_set_comments.count()
		pinned_comment_counter.append(comment_number)
	pinned_context = zip(pinned_set, pinned_comment_counter)
 
	unpinned_comment_counter = []
	for query in unpinned_set:
		article_pk = query.pk
		unpinned_set_comments = Comments.objects.filter(article_id = article_pk).order_by("-written_on")
		comment_number = unpinned_set_comments.count()
		unpinned_comment_counter.append(comment_number)
	unpinned_context = zip(unpinned_set, unpinned_comment_counter)

	context = {
		"articles": queryset,
		"community_name": h2,
		"pinned_articles": pinned_set,
		"unpinned_articles": unpinned_set,
		"community_list": community_list,
		"pinned_context": pinned_context,
		"unpinned_context": unpinned_context,
	}

	return render(request, "community_detail.html", context)

def article_view(request, article_pk, **kwargs):
	"""
	shows the contents of the article and its
	comments and likes if exist.
	"""

	object_404 = Articles.objects.filter(id = article_pk)
	if not object_404.exists():
		return redirect('community')

	community_list = Community.objects.all()
	
	queryset =  Articles.objects.get(id = article_pk)
	article_id = article_pk
	community_id = queryset.community_id
	
	queryset_comments = Comments.objects.filter(article_id = article_pk).order_by("-written_on")
	queryset_likes = Likes.objects.filter(article_id = article_pk)
	liked = Likes.objects.filter(article_id = article_pk, user_id=request.user).exists()
	comments_count = queryset_comments.count()
	likes_count = queryset_likes.count()


	context = {
		"community_list": community_list,
		"contents": queryset,
		"comments": queryset_comments,
		"comments_num" : comments_count, 
		"liked": liked, 
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

	community_list = Community.objects.all()
	queryset_user = User.objects.get(username = username)
	queryset_article = Articles.objects.filter(author_id = queryset_user)
	queryset_comment = Comments.objects.filter(user_id = queryset_user)
	article_count = len(queryset_article)
	comment_count = len(queryset_comment)
	context = {
		"community_list": community_list,
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

	community_list = Community.objects.all()
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
		"community_list": community_list,
	}

	return render(request, "register.html", context)

def login_view(request, *args, **kwargs):
	"""
	'/login' calls 'login_view'.
	'login_view' renders login page.
	The View gets username and password from the page.
	"""

	community_list = Community.objects.all()
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('community')
		else:
			messages.info(request, "Username or Password is incorrect.")

	context = {"community_list": community_list,}
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
	community_list = Community.objects.all()
	context = { "username": username,
				"community_list": community_list,
	}
	logout(request)
	return render(request, "logout.html", context)

@login_required(login_url='login')
def write_article(request, community_name, **kwargs):
	"""
	renders article writing page.
	"""

	username = request.user
	community_list = Community.objects.all()
	community = Community.objects.get(community_name = community_name)
	staff = username.is_staff
	
	if staff:
		form = ArticleForm()
	else:
		form = ArticleUserForm()
	
	if request.method == 'POST':
		if staff:
			article = Articles.objects.create(community_id = community, author_id=username)
			article.save()
			form = ArticleForm(request.POST, instance=article)
			if form.is_valid():
				article_object = form.save()
				return redirect(article_object.get_absolute_url())
		else:
			article = Articles.objects.create(community_id = community, author_id=username)
			article.save()
			form = ArticleUserForm(request.POST, instance=article)
			if form.is_valid():
				article_obj = form.save()
				return redirect(article_obj.get_absolute_url())

	context={ 
			'form': form,
			'staff': staff,
			'community_name': community_name,
			"community_list": community_list,
			}
	return render(request, "write_article.html", context)

@login_required(login_url='login')
def edit_article(request, community_name, article_pk, **kwargs):
	"""
	rendert edit windows
	"""

	try:
		article = Articles.objects.get(id=article_pk)
	except:
		community = Community.objects.get(community_name=community_name)
		return redirect(community.get_absolute_url())

	community_list = Community.objects.all()
	article = Articles.objects.get(id=article_pk)
	community = article.community_id
	staff = request.user.is_staff
	
	if staff:
		form = ArticleForm(instance=article)
	else:
		form = ArticleUserForm(instance=article)
 
	if request.method == 'POST':
		if staff:
			form = ArticleForm(request.POST, instance=article)
			if form.is_valid():
				form.save()
				return redirect(article.get_absolute_url()) 
		else:
			form = ArticleUserForm(request.POST, instance=article)
			if form.is_valid():
				form.save()
				return redirect(article.get_absolute_url())

	context = { 'form':form, 
				'article':article, 
				'community_name':community,
				"community_list": community_list,
				'article_pk': article_pk,
	}

	return render(request, 'write_article.html', context)

@login_required(login_url='login')
def delete_article(request, community_name, article_pk, **kwargs):
	""" 
 	assures whether the article should be deleted.
	On confirm the article will be deleted.
 	"""

	try:
		article = Articles.objects.get(id=article_pk)
	except:
		community = Community.objects.get(community_name=community_name)
		return redirect(community.get_absolute_url())

	community_list = Community.objects.all()
	community = article.community_id

	if request.method == 'POST':
		article.delete()
		return redirect(community.get_absolute_url())

	context = {
			'article': article, 
			'community_name': community,
			'article_pk': article_pk,
			"community_list": community_list,
	}
	return render(request, 'delete_article.html', context)

@login_required(login_url='login')
def reply_article(request, community_name, article_pk, **kwargs):
	"""
	renders form for a comment.
	"""
	
	try:
		queryset = Articles.objects.get(id=article_pk)
	except:
		community = Community.objects.get(community_name=community_name)
		return redirect(community.get_absolute_url())
	
	community_list = Community.objects.all()
	article_id = article_pk
	community_id = queryset.community_id
	queryset_comments = Comments.objects.filter(article_id = article_pk).order_by("-written_on")
	queryset_likes = Likes.objects.filter(article_id = article_pk)
	comments_count = len(queryset_comments)
	likes_count = len(queryset_likes)

	form = CommentForm()
	context = {
		"community_list": community_list,
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
def delete_comment(request, community_name, article_pk, comment_pk, **kwargs):
	"""
	delete comment
	"""

	try:
		article = Articles.objects.get(id=article_pk)
	except:
		community = Community.objects.get(community_name=community_name)
		return redirect(community.get_absolute_url())

	community_list = Community.objects.all()
	comments = Comments.objects.filter(article_id = article_pk).order_by("-written_on")
	comment = Comments.objects.filter(pk=comment_pk)
	community_name = article.community_id

	if not comment.exists():
		return redirect(article.get_absolute_url())

	context ={ 
				'article': article,
				'comments': comments,
				'community_name': community_name,
				'article_pk': article.pk,
				'comment': comment,
				"community_list": community_list,
	}

	if request.method == 'POST':
		comment.delete()
		return redirect(article.get_absolute_url())

	return render(request, 'delete_comment.html', context)

@login_required(login_url='login')
def edit_comment(request, community_name, article_pk, comment_pk, **kwargs):
	""""
	edit comment
	"""

	try:
		queryset = Articles.objects.get(id=article_pk)
	except:
		community = Community.objects.get(community_name=community_name)
		return redirect(community.get_absolute_url())

	object_404 = Comments.objects.filter(pk=comment_pk)
	if not object_404.exists():
		return redirect(queryset.get_absolute_url())	

	community_list = Community.objects.all()
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
		"comment_pk":comment_pk,
		"community_list": community_list,
	}
	
	return render(request, 'reply.html', context)

@login_required(login_url='login')
def like_button(request, article_pk, **kwargs):
	"""
	handling like button
	"""

	try:
		queryset = Articles.objects.get(id=article_pk)
	except:
		return redirect('community')

	article_id = article_pk
	username = request.user
	liked = Likes.objects.filter(article_id = article_pk, user_id=username).exists()

	if request.method == 'POST':
		if not liked :
			like_obj = Likes.objects.create(article_id=queryset, user_id=username)
			like_obj.save()
		else:
			like_obj = Likes.objects.filter(article_id=article_id, user_id=username)
			like_obj.delete()			

	return redirect(queryset.get_absolute_url())