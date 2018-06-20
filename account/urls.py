
from django.urls import path, include
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm ,password_reset_complete
from django.contrib.auth.views import password_change, password_change_done, login, logout, logout_then_login
from django.contrib.auth import views as auth_views
from . import views

app_name='account'

urlpatterns = [
	 
	 path('password-change/', password_change, name='password_change'),
	 path('password-change/done/', password_change_done, name='password_change_done'),
	 path('login/', login, name='login'),
	  path('password-reset/', auth_views.password_reset, name='password_reset'),
	  path('password-reset/done/', auth_views.password_reset_done, name='password_reset_done'),
	  path('password-reset/confirm/<uidb64>/<token>/', auth_views.password_reset_confirm, name='password_reset_confirm'),
	 
	 path('password-reset/complete/', auth_views.password_reset_complete, name='password_reset_complete'),
	 
	 
	 #path('logout/', logout, name='logout'),
	 #path('logout_then_login/', logout_then_login, name='logout_then_login'),
	 
	 

	
	
]
