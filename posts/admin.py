from django.contrib import admin
from .models import Post, Comment, Profile



# Register your models here.
class PostAdmin(admin.ModelAdmin):
	list_display = ('title', 'slug', 'user', 'publish', 'status')
	list_filter = ('status', 'posted_on', 'publish', 'user')
	search_fields = ('title', 'body')
	prepopulated_fields = {'slug': ('title',)}
	raw_id_fields = ('user',)
	date_hierarchy = 'publish'
	ordering = ['status', 'publish']
admin.site.register(Post, PostAdmin)

class CommentAdmin(admin.ModelAdmin):
	list_display = ('user', 'post', 'created', 'active')
	list_filter = ('active', 'created', 'updated')
	search_fields = ('user','body')
admin.site.register(Comment, CommentAdmin)

class ProfileAdmin(admin.ModelAdmin):
	list_display = ['user', 'date_of_birth', 'photo']
admin.site.register(Profile, ProfileAdmin)