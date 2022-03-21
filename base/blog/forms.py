from django import forms
from .models import Post

class CreatePost(forms.Form):
	headline = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control mb-3'}))
	summary = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control mb-3'}))
	body = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control mb-3'}))
	slug = forms.SlugField(help_text="Slug will automate create." ,widget=forms.TextInput(attrs={'class': 'form-control'}), required=None)

class UpdatePost(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('headline', 'summary','body', 'slug')
		widgets = {
			'headline': forms.TextInput(attrs={'class': 'form-control mb-3'}),
			'summary': forms.TextInput(attrs={'class': 'form-control mb-3'}),
			'body': forms.Textarea(attrs={'class': 'form-control mb-3'}),
			'slug': forms.TextInput(attrs={'class': 'form-control mb-3'})
		}