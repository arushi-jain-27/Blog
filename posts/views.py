from .forms import PostForm, CommentForm, UserForm, EmailPostForm, SearchForm, ProfileEditForm, SharedPostForm
from haystack.query import SearchQuerySet
from .models import Post,Comment, PostFavorite
from django.http import Http404
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.views.generic.edit import CreateView, UpdateView, DeleteView, View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count
from slugify import slugify
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required

@login_required
def link_post(request):
	if request.method == 'POST':
		# form is sent
		form = SharedPostForm(data=request.POST)
		if form.is_valid():
			# form data is valid
			cd = form.cleaned_data
			tags = cd['tags']
			new_item = form.save(commit=False)
			# assign current user to the item
			#new_item.slug = slugify('title')
			new_item.user = request.user
			new_item.save()
			for tag in tags:
				new_item.tags.add(tag)
			messages.success(request, 'Post added successfully')
			# redirect to new created item detail view
			return redirect(new_item.get_absolute_url())
	else:
	# build form with data provided by the bookmarklet via GET
		form = SharedPostForm(data=request.GET)
		return render(request,'posts/link_post.html',{'section': 'images','form': form})

def edit(request):
	if request.method == 'POST':	
		profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
		if profile_form.is_valid():
			profile_form.save()
			messages.success(request, 'Profile updated successfully')
	else:		
		profile_form = ProfileEditForm(instance=request.user.profile)
		messages.error(request, 'Error updating your profile')
	return render(request, 'posts/edit.html', {'profile_form': profile_form})

def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'posts/login.html', context)

def login_user (request, tag_slug = None):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate (username=username, password=password)
		if user is not None:
			if user.is_active:
				login (request, user)
				all_posts = Post.objects.filter(user=request.user, status="published")

				tag = None
				if tag_slug:
					tag = get_object_or_404 (Tag, slug=tag_slug)
					all_posts = all_posts.filter(tags__in =[tag])
				paginator = Paginator (all_posts, 10)
				page = request.GET.get('page')
				try:
					posts = paginator.page(page)
				except PageNotAnInteger:
					posts = paginator.page(1)
				except EmptyPage:
					posts = paginator.page(paginator.num_pages)
				return render (request, "posts/dashboard.html",{'drafts':Post.objects.filter(user=request.user, status="draft"), 'page': page, 'all_posts': posts, 'tag': tag, 'profile':user.profile})
			else:
				return render (request, 'posts/login.html', {'error_message': 'Your account has been disabled'})
		else:
			return render (request, 'posts/login.html', {'error_message': 'Invalid login'})
	return render(request, 'posts/login.html')



def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                post = Post.objects.filter(user=request.user)
                return render(request, 'posts/index.html', {'all_posts': post})
    context = {
        "form": form,
    }
    return render(request, 'posts/register.html', context)

def create_post(request):
    if not request.user.is_authenticated:
        return render(request, 'posts/login.html')
    else:
        form = PostForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            tags = form.cleaned_data['tags']
            post = form.save(commit=False)
            post.user = request.user
            post.image = request.FILES['image']
            post.slug=slugify ('title')
            post.save()
            for tag in tags:
                post.tags.add(tag)
            return render(request, 'posts/details.html', {'post': post})
        context = {
            "form": form,
        }
        return render(request, 'posts/create_post.html', context)
		

		
class update_post(UpdateView):
	model=Post
	fields=['title', 'description', 'body', 'image']
	
class update_comment(UpdateView):
	model=Comment
	fields=['body']

def create_comment(request, post_id):
	if not request.user.is_authenticated:
		return render (request,'posts/login.html')
	else:
		form = CommentForm(request.POST or None, request.FILES or None)
		
		post = get_object_or_404(Post, pk=post_id)
		comments = post.comment_set.filter(active=True)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.post = post
			comment.user = request.user
			comment.save()
			return render(request, 'posts/details.html', {'post': post,'new_comment': comment, 'comments':comments})
		context = {
			'post': post,
			'form': form,
		}
		return render(request, 'posts/create_comment.html', context)

def add_favorite (request, post_id):
	if not request.user.is_authenticated:
		return render (request,'posts/login.html')
	else:
		post = get_object_or_404(Post, pk=post_id)
		comments = post.comment_set.filter(active=True)
		#bookmark, created = PostFavorite.objects.get_or_create(user=request.user, post=post)
		bookmark = PostFavorite.objects.filter(user=request.user, post=post)
		
		if bookmark:
			bookmark.delete()
		else:
			bookmark=PostFavorite(user=request.user, post=post)
			bookmark.save()
		return render(request, 'posts/details.html', {'post': post, 'bookmark':bookmark, 'comments':comments})


def delete_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    post.delete()
    post = Post.objects.filter(user=request.user)
    return render(request, 'posts/index.html', {'all_posts': post})


def delete_comment(request, post_id, comment_id):
    post = get_object_or_404(Post, pk=post_id)
    comment = Comment.objects.get(pk=comment_id)
	#comments = post.comment_set.filter (active = True)
    comment.delete()
    return render(request, 'posts/details.html', {'post': post,'comments': post.comment_set.filter (active = True)}) 

def index (request, tag_slug=None):
	all_posts=Post.objects.filter(status="published")
	tag=None
	if tag_slug:
		tag=get_object_or_404 (Tag, slug=tag_slug)
		all_posts=all_posts.filter (tags__in=[tag])
		
	paginator = Paginator(all_posts, 10) # 10 posts in each page
	page = request.GET.get('page')
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer deliver the first page
		posts = paginator.page(1)
	except EmptyPage:
		# If page is out of range deliver last page of results
		posts = paginator.page(paginator.num_pages)
	#return render(request,'posts/index.html',{'all_posts': all_posts})
	return render(request, 'posts/index.html', {'page': page, 'all_posts': posts,'tag':tag})


def detail(request, year, month, day, post):
    if not request.user.is_authenticated:
        return render(request, 'posts/login.html')
    else:
        user = request.user
        post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month, publish__day=day)
		
        post_tags_ids = post.tags.values_list('id', flat=True)
        similar_posts = Post.objects.filter(status="published", tags__in=post_tags_ids).exclude(id=post.id)
        similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')
		
        return render(request, 'posts/details.html', {'post': post, 'user': user, 'comments':post.comment_set.filter(active=True),'similar_posts': similar_posts })

			
		
def post_share(request, post_id):
	# Retrieve post by id
	post = get_object_or_404(Post, id=post_id, status='published')
	sent=False
	if request.method == 'POST':
	# Form was submitted
		form = EmailPostForm(request.POST)
		if form.is_valid():
			# Form fields passed validation
			cd = form.cleaned_data
			post_url = request.build_absolute_uri(post.get_absolute_url())
			subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
			message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
			send_mail(subject, message, 'admin@myblog.com',[cd['to']])
			sent = True
		return render(request, 'posts/share.html', {'post': post,'form': form,'sent':sent,'cd':cd})
			# ... send email
	else:
		form = EmailPostForm()
		return render(request, 'posts/share.html', {'post': post,'form': form,'sent':sent})
		
def post_search(request):
    form = SearchForm()
    #return render(request, 'posts/search.html', {'form': form})
    if 'query' in request.GET:        
        form = SearchForm(request.GET)
        if form.is_valid():
            cd = form.cleaned_data
            results = Post.objects.filter(Q(title__icontains=cd['query'])|Q(user__username__icontains=cd['query'] )| Q(tags__name__icontains=cd['query']) ).distinct()
            
            #results = Post.objects.all()
            #results = SearchQuerySet().models(Post).filter(content=cd['query']).load_all()
            # count total results
            total_results = results.count()
            return render(request, 'posts/search.html', {'form': form,'cd': cd, 'results': results,'total_results': total_results})
    else:
        #form=SearchForm ()
        return render(request, 'posts/search.html', {'form': form})
		
def change_password(request):
	if not request.user.is_authenticated:
		return render(request, 'posts/login.html')
	else:
		if request.method == "POST":
			
			form = PasswordChangeForm(request.user, request.POST)
			
			if form.is_valid():
				user = form.save()
				update_session_auth_hash(request, user)  # Important!
				messages.success(request, 'Your password was successfully updated!')
				#post = Post.objects.filter(user=request.user)
				return render(request, 'posts/password_change_done.html', {'message': 'password changed'})
			else:
				messages.error(request, 'Please correct the error below.')
		else:
			
			form = PasswordChangeForm(request.user)
			
			return render(request, 'posts/password_change_form.html', {'form': form  })

	

	