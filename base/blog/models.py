from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse

# Create your models here.
class Post(models.Model):
	headline = models.CharField(max_length=50)
	summary = models.CharField(max_length=150, null=True)
	body = models.TextField()
	date = models.DateTimeField(auto_now_add=True)
	slug = models.SlugField(max_length=80, null=True)

	def __str__(self):
		return self.headline
		
	def get_absolute_url(self):
		return reverse('blog:post_detail_page', kwargs={'slug': self.slug})
	
	def save(self, *args, **kwargs): # new
		if self.slug == None:
			slug = slugify(self.headline)

			has_slug = Post.objects.filter(slug=slug).exists()
			i = 1
			while has_slug:
				i += 1
				slug = slugify(self.headline) + '-' + str(i)
				has_slug = Post.objects.filter(slug=slug).exists()
			self.slug = slug

		return super().save(*args, **kwargs)

class Category(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name