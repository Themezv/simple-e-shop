from django import forms


from .models import Page

class PageForm(forms.ModelForm):
	class Meta:
		model = Page
		fields = [
			'name',
			'title',
			'description',
			'menu',
			'tile',
			'avatar',
		]