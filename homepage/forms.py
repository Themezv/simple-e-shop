from django import forms



from .models import Page
from django.contrib.flatpages.models import FlatPage


class AboutForm(forms.ModelForm):
	class Meta:
		model = FlatPage
		fields = [
			'title',
			'content',
		]


class ContactForm(forms.ModelForm):
	class Meta:
		model = FlatPage
		fields = [
			'title',
			'content',
		]
