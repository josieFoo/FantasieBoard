from django.shortcuts import render
from django.http import HttpResponse
from .models import *
# Create your views here.
def home_view(request, *args, **kwargs):
	"""
	home controller
	"""
	#print(request, args, kwargs)
	return render(request, "index.html", {})

def community_view(request, *args, **kwargs):
	"""
	Shows a list of communities which be joined by users.
	'community.html' extends 'index.html'.
	"""
	A=[]
	for item in ['a', 'b', 'c']:
		A.append(item)
	context = {'community_list': A}
	return render(request, "community.html", context)

def community_create(request, *args, **kwargs):
	...

def user_create(request, *args, **kwargs):
	...
	