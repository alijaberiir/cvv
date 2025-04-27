from django import forms
from .models import comments
from django.utils.translation import gettext_lazy as _

from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox



class comments_form(forms.ModelForm):
	captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox, required=True)

	class Meta:
		model = comments
		fields = ['full_name', 'email', 'comments', 'blog_id']


	def __init__(self, *args, **kwargs):
		blog_id = kwargs.pop('blog_id', None)
		super().__init__(*args, **kwargs)

		# Autofill for blog_id and lang
		if blog_id:
			self.fields['blog_id'].initial = blog_id
	   

		# Add common attrs
		for field in self.visible_fields():
			field.field.widget.attrs['placeholder'] = field.label
			field.field.widget.attrs['required'] = 'required'
		
		self.fields['comments'].widget.attrs.update({'rows': 4, 'maxlength': 300})
		self.fields['email'].widget.attrs['class'] = 'c-email'
		

	def clean_comments(self):
		comments = self.cleaned_data.get('comments')
		if comments and len(comments) > 300:
			raise forms.ValidationError(_('Comment must be at most 300 characters long.'))
		return comments