from django.contrib.auth.models import User
from django import forms
from .models import Post, Comment, PostFavorite, Profile
from taggit.forms import *
from urllib import request
from django.core.files.base import ContentFile
from django.utils.text import slugify

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

class SharedPostForm(forms.ModelForm):
	tags = TagField()
	class Meta:
		model=Post
		fields =['title', 'url', 'description', 'body', 'tags', 'status']
	def clean_url(self):
		url = self.cleaned_data['url']
		valid_extensions = ['jpg', 'jpeg']
		extension = url.rsplit('.', 1)[1].lower()
		if extension not in valid_extensions:
			raise forms.ValidationError('The given URL does not match valid image extensions.')
		return url
	def save(self, force_insert=False,force_update=False,commit=True):
		image = super(SharedPostForm, self).save(commit=False)
		image_url = self.cleaned_data['url']
		image_name = '{}.{}'.format(slugify(image.title),image_url.rsplit('.', 1)[1].lower())
		response = request.urlopen(image_url)
		#image.slug.save (slugify(image.title), save=False)
		image.slug = slugify(image.title)
		image.image.save(image_name, ContentFile(response.read()), save=False)
		if commit:
			image.save()
		return image



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
	
class ProfileEditForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('name', 'date_of_birth', 'photo')