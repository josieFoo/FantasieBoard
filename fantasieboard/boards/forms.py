from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
#from django.forms.widgets import HiddenInput

from .models import Articles, Comments

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
		fields = '__all__' #['title', 'rich_txt']
		#widgets = {
		#	'community_id': forms.HiddenInput(),
		#	'author_id': forms.HiddenInput(),
		#}

class CommentForm(ModelForm):
    """ 
    Form for a comment.
    """
    
    class Meta:
        model = Comments
        fields = '__all__' # ['rich_txt']
        widgets = { 'article_id': forms.HiddenInput(), 
                    'user_id': forms.HiddenInput(), 
        }