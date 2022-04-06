from django import forms
from .models import Post, Category, Tag

class CreatePost(forms.Form):
	headline = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control mb-3'}))
	summary = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control mb-3'}))
	body = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control mb-3'}))
	category = forms.ModelChoiceField(
		queryset=Category.objects.all(), 
		widget=forms.Select(attrs={'class': 'form-control mb-3'})
	)
	slug = forms.SlugField(help_text="Slug will automate create." ,widget=forms.TextInput(attrs={'class': 'form-control'}), required=None)

class UpdatePost(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('headline', 'summary','body', 'category', 'slug')
		widgets = {
			'headline': forms.TextInput(attrs={'class': 'form-control mb-3'}),
			'summary': forms.TextInput(attrs={'class': 'form-control mb-3'}),
			'body': forms.Textarea(attrs={'class': 'form-control mb-3'}),
			'category': forms.Select(attrs={'class': 'form-control mb-3'}),
			'slug': forms.TextInput(attrs={'class': 'form-control mb-3'}),
		}

class TagForm(forms.Form):
	tags = forms.ModelMultipleChoiceField(
		queryset = Tag.objects.all(),
		required = False,
		widget = forms.CheckboxSelectMultiple(),
	)

class CategoryTagControlForm(forms.Form):
	TYPE = (
        ('Category', 'Category'),
        ('Tag', 'Tag'),
	)
	type = forms.ChoiceField(choices=TYPE, widget=forms.Select(attrs={'class': 'form-select mb-3'}))
	name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control mb-3'}))
	