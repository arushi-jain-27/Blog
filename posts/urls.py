
from django.urls import path, include

from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm ,password_reset_complete
from . import views
"""
	path('',views.IndexView.as_view(), name='index' ),
	path('register/',views.UserFormView.as_view(), name='register' ),
	path('<pk>/', views.DetailView.as_view(),name='detail'),
	path ('posts/add/', views.PostCreate.as_view(), name='post-add'),
	path ('posts/<pk>/', views.PostUpdate.as_view(), name='post-update'),
	path ('posts/<pk>/delete/', views.PostDelete.as_view(), name='post-delete'),   
"""
app_name='posts'

urlpatterns = [
	 
	 path('tag/<tag_slug>',views.index, name='post_list_by_tag' ),
	 path('',views.index, name='index' ),	 
	 path('favorite/<post_id>', views.add_favorite, name='add_favorite'),
	 path('create_post/', views.create_post, name='create_post'),
	 path ('link_post/', views.link_post, name='link_post'),
	 path('update_post/<pk>', views.update_post.as_view(), name='update_post'),
	 path('update_comment/<pk>', views.update_comment.as_view(), name='update_comment'),
	 path('<post_id>/create_comment/', views.create_comment, name='create_comment'),
	 path('<post_id>/delete_post/', views.delete_post, name='delete_post'),
	 path('<post_id>/delete_comment/<comment_id>', views.delete_comment, name='delete_comment'),
	 path ('register/', views.register, name='register'),
	 path ('edit/', views.edit, name='edit'),
	 path('password_reset/', password_reset, name='password_reset'),
	 
	 path('password_reset_complete/', password_reset_complete, name='password_reset_complete'),
	 path('password_reset_confirm/<uidb64>/<token>/', password_reset_confirm, name='password_reset_confirm'),
	 path('password_reset/done/', password_reset_done, name='password_reset_done'),
	 
	 path ('login_user/', views.login_user, name='login_user'),
	 path ('logout_user/', views.logout_user, name='logout_user'),
	 path('<post_id>/share/', views.post_share,name='post_share'),
	 path('search/', views.post_search, name='post_search'),
	 path('password-change/', views.change_password, name='password_change'),
	 #path('password-change/done/', password_change_done, name='password_change_done'),
	 
	 #path('<post_id>/', views.detail, name='detail'),
	 path('<year>/<month>/<day>/<post>', views.detail, name='detail'),
	 path ('user_list', views.user_list, name = "user_list"),
	 path ('user_follow/<to>', views.user_follow, name = "user_follow"),
	 path ('user_detail/<username>', views.user_detail, name = "user_detail"),
	 path ('dashboard', views.dashboard, name = "dashboard")

	 #path('<Post_id>/favorite', views.favorite, name='favorite'),

	
	
]
