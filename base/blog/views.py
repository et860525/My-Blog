from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from .models import Post, Category
from .forms import CreatePost, UpdatePost, CategoriesForm

# Create your views here.
def home_page(request):
	posts = Post.objects.all().order_by('-date')
	categories = Category.objects.all()

	paginator = Paginator(posts, 6)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	context = {'posts': page_obj, 'categories': categories}

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
	posts = Post.objects.all().order_by('-date')

	categories_form = CategoriesForm()

	paginator = Paginator(posts, 6)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	if request.method == 'POST':
		form = CategoriesForm(request.POST)
		if form.is_valid():
			# Get categories checkbox 'ckecked' / 獲取打勾的 checkbox
			categories = form.cleaned_data['categories']
			# Make every categories to convert string / 把 categories裡的元素轉化成 string
			categories = [category.name for category in categories]

			# Check categories list is exists or not / 確認 categories list是否存在
			if categories:
				filtered_post = []
				if len(categories) == 1:
					# Retrun posts of one categories / 只有一個 category就直接回傳
					filtered_post = Post.objects.filter(category__name=categories[0]).order_by('-date')
				else:
					# Get(pop) first category to filter post / 先獲得第一個 element所 filter的 posts
					first_category = categories.pop(0)
					first_filter_posts = Post.objects.filter(category__name=first_category)

					# Loop every categories do filter / 將剩下的 categories一個一個做 filter
					for category in categories:
						ps = first_filter_posts.filter(category__name=category).order_by('-date')
						filtered_post = []
						filtered_post = ps
						first_filter_posts = ps

				paginator = Paginator(filtered_post, 6)
				page_number = request.GET.get('page')
				page_obj = paginator.get_page(page_number)
			else:
				redirect('blog:categories_page')

	context = {'categories': categories, 'categories_form': categories_form, 'posts': page_obj}
	
	return render(request, 'blog/categories.html', context)

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
