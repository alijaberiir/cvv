from django import forms
from .models import Contact

from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox


class contact(forms.ModelForm):
	captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox,required=True)
	def __init__(self, *args, **kwargs):
		super(contact, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['required'] = 'required'
			visible.field.widget.attrs['placeholder'] = visible.label
			self.fields['massages'].widget.attrs.update({'rows': 3})
			self.fields['email'].widget.attrs['class'] = 'c-email'
			self.fields['captcha'].widget.attrs['required'] = 'required'
	class Meta:
		model = Contact
		exclude = ('created',)