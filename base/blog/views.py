from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from .models import Post, Category, Tag
from .forms import CreatePost, UpdatePost, TagForm

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

def tags_page(request):
	tags = Tag.objects.all()
	posts = Post.objects.all().order_by('-date')

	tag_form = TagForm()

	paginator = Paginator(posts, 6)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	if request.method == 'POST':
		form = TagForm(request.POST)
		if form.is_valid():
			# Get tags checkbox 'ckecked' / 獲取打勾的 checkbox
			tags = form.cleaned_data['tags']
			# Make every tags to convert string / 把 tags裡的元素轉化成 string
			tags = [tag.name for tag in tags]

			# Check tags list is exists or not / 確認 tags list是否存在
			if tags:
				filtered_post = []
				if len(tags) == 1:
					# Retrun posts of one tags / 只有一個 tag就直接回傳
					filtered_post = Post.objects.filter(tag__name=tags[0]).order_by('-date')
				else:
					# Get(pop) first tag to filter post / 先獲得第一個 element所 filter的 posts
					first_tag = tags.pop(0)
					first_filter_posts = Post.objects.filter(tag__name=first_tag)

					# Loop every tags do filter / 將剩下的 tags一個一個做 filter
					for tag in tags:
						ps = first_filter_posts.filter(tag__name=tag).order_by('-date')
						filtered_post = []
						filtered_post = ps
						first_filter_posts = ps
					
				tag_form = TagForm(request.POST)

				paginator = Paginator(filtered_post, 6)
				page_number = request.GET.get('page')
				page_obj = paginator.get_page(page_number)
			else:
				redirect('blog:tags_page')

	context = {'tag_form': tag_form, 'posts': page_obj}
	
	return render(request, 'blog/tags.html', context)

@login_required
def dashboard(request):
	posts = Post.objects.all().order_by('-date')

	return render(request, 'blog/dashboard.html', {'posts': posts})

# Create Post
@login_required
def post_create(request):
	form = CreatePost()
	tag_form = TagForm()
	
	if request.method == 'POST':
		form = CreatePost(request.POST)
		tag_form = TagForm(request.POST)
		
		if form.is_valid() and tag_form.is_valid():
			# Get form data
			headline = form.cleaned_data['headline']
			summary = form.cleaned_data['summary']
			body = form.cleaned_data['body']
			category = form.cleaned_data['category']
			tags = tag_form.cleaned_data['tags']

			if not Post.objects.filter(headline=headline).exists():
				post = Post(headline=headline, summary=summary, body=body, category=category)
				post.save()

				# Make every tags to convert string
				tags = [tag for tag in tags]

				tags = Tag.objects.filter(name__in=tags)

				for tag in tags:
					tag.posts.add(post)

				return redirect('blog:blog_dashboard_page')
			else:
				print('Headline exist')
				return redirect('blog:blog_dashboard_page')					

	context = {'form': form, 'tag_form': tag_form}
	return render(request, 'blog/post_form.html', context)

# Update Post
@login_required
def post_update(request, slug):
	post = Post.objects.get(slug=slug)
	post_tags = Tag.objects.filter(posts__headline__startswith=post.headline)

	form = UpdatePost(instance=post)
	tag_form = TagForm(initial={'tags': post_tags})

	if request.method == 'POST':
		form = UpdatePost(request.POST, instance=post)
		tag_form = TagForm(request.POST)
		if form.is_valid() and tag_form.is_valid():
			form.save()

			# Get checkbox status
			tags = tag_form.cleaned_data['tags']
			# Make every tags to convert string
			tags = [tag for tag in tags]

			# Get tags when checkbox is enabling
			add_tags = Tag.objects.filter(name__in=tags)
			# Get tags when checkbox is not enabling
			del_tags = Tag.objects.exclude(name__in=tags)

			for tag in add_tags:
				tag.posts.add(post)

			for tag in del_tags:
				tag.posts.remove(post)

		return redirect('blog:blog_dashboard_page')

	return render(request, 'blog/post_form.html', {'form': form, 'tag_form': tag_form})

# Delete Post
@login_required
def post_delete(request, slug):
	post = Post.objects.get(slug=slug)
	
	if request.method == 'POST':
		post.delete()
		return redirect('blog:blog_dashboard_page')

	return render(request, 'blog/post_delete.html', {'post': post})
