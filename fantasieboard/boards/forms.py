from django import forms
from django.db.models import forms
from django import forms
from models import *

class UserForm(forms.ModelForm):
	class Meta:
		model = Users
		widgets = {
			'password': forms.PasswordInput(),
		}