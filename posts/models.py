from django.db import models
from django.contrib.auth.models import Permission, User
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
import datetime
from taggit.managers import TaggableManager
# Create your models here.

class Profile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	name = models.CharField (max_length=30, default="Anonymous")
	date_of_birth = models.DateField(blank=True, null=True)
	photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)
	def __str__(self):
		return 'Profile for user {}'.format(self.user.username)

class Post (models.Model):
	user=models.ForeignKey(User, on_delete=models.CASCADE)
	STATUS_CHOICES = (('draft', 'Draft'),('published', 'Published'),)
	slug = models.SlugField(max_length=250, unique_for_date='publish', default='')
	publish = models.DateTimeField(default=timezone.now)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
	title=models.CharField(max_length=50)
	description=models.CharField (max_length=100)
	body=models.TextField ()
	posted_on=models.DateTimeField (auto_now_add=True)
	modified_on=models.DateTimeField (auto_now=True)
	image=models.FileField()
	tags = TaggableManager()
	class Meta:
		ordering = ('-publish',)
	def get_absolute_url(self):
		return reverse ('posts:detail', args=[self.publish.year, self.publish.strftime('%m'), self.publish.strftime('%d'), self.slug])
	
	def __str__ (self):
		return self.title+'-'+self.description
	
class Comment (models.Model):
	user=models.ForeignKey(User, on_delete=models.CASCADE)
	post=models.ForeignKey (Post, on_delete=models.CASCADE)
	body=models.TextField()	
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	active = models.BooleanField(default=True)	
	class Meta:
		ordering = ('created',)
	def __str__ (self):
		return self.user.username+':'+self.body
	def get_absolute_url(self):
		#return reverse ('posts:detail', kwargs={'pk':self.post.pk})
		return reverse ('posts:index')
		



class PostFavorite (models.Model):
	user=models.ForeignKey(User, on_delete=models.CASCADE)
	post=models.ForeignKey (Post, on_delete=models.CASCADE)
	def get_absolute_url(self):
		#return reverse ('posts:detail', kwargs={'pk':self.post.pk})
		return reverse ('posts:index')
	
	
	
# Create your models here.
