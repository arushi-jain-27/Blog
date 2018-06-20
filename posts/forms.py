from django.contrib.auth.models import User
from django import forms
from .models import Post, Comment, PostFavorite
from taggit.forms import *

class UserForm (forms.ModelForm):
	password=forms.CharField(widget=forms.PasswordInput)
	
	class Meta:
		model=User
		fields=['username','email','password']
	
class PostForm(forms.ModelForm):
	tags = TagField()
	class Meta:
		model = Post
		fields = ['title', 'description', 'body', 'image', 'tags', 'status']


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['body']

class EmailPostForm(forms.Form):
	name = forms.CharField(max_length=25)
	email = forms.EmailField()
	to = forms.EmailField()
	comments = forms.CharField(required=False, widget=forms.Textarea)

class SearchForm(forms.Form):
	query = forms.CharField()