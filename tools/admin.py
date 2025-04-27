from django.contrib import admin
from tools.models import *
from tinymce.widgets import TinyMCE
from django.db import models
from unfold.admin import ModelAdmin
from django import forms
from django.utils.safestring import mark_safe
from .utils import SELECT_ICONS
from django.utils.translation import gettext_lazy as _



class ClientsAdmin(ModelAdmin):
	list_display = [ 'name_en', 'link', 'status']
	ordering = ['status']
	list_filter = ('status',)




class SocialForm(forms.ModelForm):
	class Meta:
		model = Social
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		choices = [
			(val, mark_safe(f'<div class="social-radio">{val} {svg}</div>')) 
			for val, svg in SELECT_ICONS
		]

		self.fields['icon'].widget = forms.RadioSelect(choices=choices, attrs={'class': 'social-icon-radio'})


class SocialAdmin(ModelAdmin):
	list_display = ['link', 'icon_svg', 'status']
	ordering = ['status']
	list_filter = ('status',)
	form  = SocialForm

class ContactInfoAdmin(ModelAdmin):
	list_display = ['phone', 'email']
	ordering = ['phone',]
	


admin.site.register(Clients,ClientsAdmin)
admin.site.register(Social,SocialAdmin)
admin.site.register(ContactInfo,ContactInfoAdmin)