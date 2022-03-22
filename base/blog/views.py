from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from .models import Post
from .forms import CreatePost, UpdatePost

# Create your views here.
def home_page(request):
	posts = Post.objects.all().order_by('-date')

	return render(request, 'blog/index.html', {'posts': posts})

def about_page(request):
	return render(request, 'blog/about.html', {})

def contact_page(request):
	return render(request, 'blog/contact.html', {})

def post_page(request, slug):
	post = Post.objects.get(slug=slug)

	return render(request, 'blog/post.html', {'post': post})

@login_required
def dashboard(request):
	posts = Post.objects.all()

	return render(request, 'blog/dashboard.html', {'posts': posts})

# Create Post
@login_required
def post_create(request):
	form = CreatePost()
	
	if request.method == 'POST':
		form = CreatePost(request.POST)
		
		if form.is_valid():
			# Get form data
			headline = form.cleaned_data['headline']
			summary = form.cleaned_data['summary']
			body = form.cleaned_data['body']

			if not Post.objects.filter(headline=headline).exists():
				post = Post(headline=headline, summary=summary, body=body)
				post.save()

				return redirect('blog:blog_dashboard_page')
			else:
				print('Headline exist')
				return redirect('blog:blog_dashboard_page')
	

	return render(request, 'blog/post_form.html', {'form': form})

# Update Post
@login_required
def post_update(request, slug):
	post = Post.objects.get(slug=slug)
	form = UpdatePost(instance=post)

	if request.method == 'POST':
		form = UpdatePost(request.POST, instance=post)
		if form.is_valid():
			form.save()
		return redirect('blog:blog_dashboard_page')

	return render(request, 'blog/post_form.html', {'form': form})

# Delete Post
@login_required
def post_delete(request, slug):
	post = Post.objects.get(slug=slug)
	
	if request.method == 'POST':
		post.delete()
		return redirect('blog:blog_dashboard_page')

	return render(request, 'blog/post_delete.html', {'post': post})
