from django import template
register = template.Library()
from ..models import Post
from django.db.models import Count

@register.simple_tag
def get_most_commented_posts(count=3):
	return Post.objects.filter(status="published").annotate(total_comments=Count('comment')).order_by('-total_comments')[:count]

@register.simple_tag
def total_posts():
	return Post.objects.filter(status="published").count()
	
@register.inclusion_tag('posts/latest_posts.html')
def show_latest_posts(count=3):
	latest_posts = Post.objects.filter(status="published").order_by('-publish')[:count]
	return {'latest_posts': latest_posts}