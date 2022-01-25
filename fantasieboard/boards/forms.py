from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Articles

class RegisterUserForm(UserCreationForm):
	"""
	extends the default 'UserCreationForm'.
	"""

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2' ]


class ArticleForm(ModelForm):
	"""
	form for writing a article.
	"""
	
	class Meta:
		model = Articles
		fields = '__all__' # testing