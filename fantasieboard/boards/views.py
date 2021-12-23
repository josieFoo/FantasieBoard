from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home_view(request, *args, **kwargs):
	"""
 	home controller
 	routed to community list on click?
  	"""
	#print(request, args, kwargs)
	return render(request, "index.html", {})

def community_view(request, *args, **kwargs):
	"""
	shows a link list of communities
	"""
	return HttpResponse("<h1> List of communities </h1>")

def community_create(request, *args, **kwargs):
	...

def user_create(request, *args, **kwargs):
	...
	