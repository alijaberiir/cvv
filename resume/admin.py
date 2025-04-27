from django.contrib import admin
from .models import Part,Contact
from tinymce.widgets import TinyMCE
from django.db import models
from unfold.admin  import ModelAdmin
from django.utils.translation import gettext_lazy as _




class PartAdmin(ModelAdmin):

	fieldsets = (
		(_("Persian section"), {
			"classes": ["tab"],
			"fields": ["part_name_fa","title_fa","sub_title_fa","description_fa","image_fa","link_name_fa"]
		}),
		(_("English section"), {
			"classes": ["tab"],
			"fields": ["part_name_en","title_en","sub_title_en","description_en","image_en"],
		}),
		(_("Settings"), {
			"classes": ["tab"],
			"fields": ["positions","rtl_or_ltr","link","status"],
		}),
	)

	list_display = ['part_name_en','part_name_fa','created','status','rtl_or_ltr','positions']
	ordering = ['positions']
	search_fields = ('part_name_en','title_en','part_name_fa','title_fa')
	list_filter=('rtl_or_ltr','status','created')
	list_editable = ('status','rtl_or_ltr','positions')
	formfield_overrides = {
		models.TextField: {'widget': TinyMCE()}
	}
admin.site.register(Part,PartAdmin)


class ContactAdmin(ModelAdmin):
	list_display = ['full_name', 'email','created']
	ordering = ['-created']
	list_filter = ('created',)

admin.site.register(Contact,ContactAdmin)