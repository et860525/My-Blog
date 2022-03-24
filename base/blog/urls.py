from django.urls import path
from blog import views

app_name = 'blog'
urlpatterns = [
	path('', views.home_page, name='home_page'),
	path('about/', views.about_page, name='about_page'),
	path('contact/', views.contact_page, name='contact_page'),
	path('dashboard/', views.dashboard, name='blog_dashboard_page'),
	path('post/<slug:slug>/', views.post_page, name='post_detail_page'),
	path('categories/', views.categories_page, name='categories_page'),
	# Post create, delete, update
	path('create-post/', views.post_create, name='post_create_page'),
	path('delete-post/<slug:slug>/', views.post_delete, name='post_delete_page'),
	path('update-post/<slug:slug>/', views.post_update, name='post_update_page'),
]