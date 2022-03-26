from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from .models import Post, Category
from .forms import CreatePost, UpdatePost, CategoriesForm

# Create your views here.
def home_page(request):
	posts = Post.objects.all().order_by('-date')

	paginator = Paginator(posts, 6)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	context = {'posts': page_obj}

	return render(request, 'blog/index.html', context)

def about_page(request):
	return render(request, 'blog/about.html', {})

def contact_page(request):
	return render(request, 'blog/contact.html', {})

def post_page(request, slug):
	post = Post.objects.get(slug=slug)

	return render(request, 'blog/post.html', {'post': post})

def categories_page(request):
	categories = Category.objects.all()
	
	return render(request, 'blog/categories.html', {'categories': categories})

@login_required
def dashboard(request):
	posts = Post.objects.all()

	return render(request, 'blog/dashboard.html', {'posts': posts})

# Create Post
@login_required
def post_create(request):
	form = CreatePost()
	categories_form = CategoriesForm()
	
	if request.method == 'POST':
		form = CreatePost(request.POST)
		categories_form = CategoriesForm(request.POST)
		
		if form.is_valid() and categories_form.is_valid():
			# Get form data
			headline = form.cleaned_data['headline']
			summary = form.cleaned_data['summary']
			body = form.cleaned_data['body']
			categories = categories_form.cleaned_data['categories']

			if not Post.objects.filter(headline=headline).exists():
				post = Post(headline=headline, summary=summary, body=body)
				post.save()

				# Make every categories to convert string
				categories = [category for category in categories]

				categories = Category.objects.filter(name__in=categories)

				for category in categories:
					category.posts.add(post)

				return redirect('blog:blog_dashboard_page')
			else:
				print('Headline exist')
				return redirect('blog:blog_dashboard_page')					

	return render(request, 'blog/post_form.html', {'form': form, 'categories_form': categories_form})

# Update Post
@login_required
def post_update(request, slug):
	post = Post.objects.get(slug=slug)
	post_categories = Category.objects.filter(posts__headline__startswith=post.headline)

	form = UpdatePost(instance=post)
	categories_form = CategoriesForm(initial={'categories': post_categories})
	

	if request.method == 'POST':
		form = UpdatePost(request.POST, instance=post)
		categories_form = CategoriesForm(request.POST)
		if form.is_valid() and categories_form.is_valid():
			form.save()

			# Get checkbox status
			categories = categories_form.cleaned_data['categories']
			# Make every categories to convert string
			categories = [category for category in categories]

			# Get categories when checkbox is enabling
			add_categories = Category.objects.filter(name__in=categories)
			# Get categories when checkbox is not enabling
			del_categories = Category.objects.exclude(name__in=categories)

			for category in add_categories:
				category.posts.add(post)

			for category in del_categories:
				category.posts.remove(post)

		return redirect('blog:blog_dashboard_page')

	return render(request, 'blog/post_form.html', {'form': form, 'categories_form': categories_form})

# Delete Post
@login_required
def post_delete(request, slug):
	post = Post.objects.get(slug=slug)
	
	if request.method == 'POST':
		post.delete()
		return redirect('blog:blog_dashboard_page')

	return render(request, 'blog/post_delete.html', {'post': post})
