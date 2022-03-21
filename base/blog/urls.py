from django.urls import path
from blog import views

app_name = 'blog'
urlpatterns = [
	path('', views.home_page, name='home_page'),
	path('dashboard/', views.dashboard, name='blog_dashboard_page'),
	path('post/<slug:slug>/', views.post_page, name='post_detail_page'),
	# Post create, delete, update
	path('create-post/', views.post_create, name='post_create_page'),
	path('delete-post/<slug:slug>/', views.post_delete, name='post_delete_page'),
	path('update-post/<slug:slug>/', views.post_update, name='post_update_page'),
]