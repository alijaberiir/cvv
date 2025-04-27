from django.db import models
from django.utils.translation import gettext_lazy as _
from meta.models import ModelMeta
from django.utils.translation import get_language
from django.utils.text import Truncator
from django.utils.html import strip_tags


class PartManager(models.Manager):
	def active(self):
		return self.filter(status = True)

class Part(ModelMeta, models.Model):
	RTLORLTR = (
		('rtl', _('Right To Left')),
		('ltr', _('Left To Right')),
	)
	"""
	part name of index page and set link name
	"""
	part_name_fa = models.CharField(_('PartName Persian'), max_length=100, blank=False, null=False, unique=True)
	part_name_en = models.CharField(_('PartName English'), max_length=100, blank=False, null=False, unique=True)
	"""
	title persian and english in first field on index
	"""
	title_fa = models.CharField(_('Title Persian'), blank=True, null=True, max_length=250,)
	title_en = models.CharField(_('Title English'), blank=True, null=True, max_length=250,)
	"""
	nuder title text
	"""
	sub_title_fa = models.CharField(_('Sub Title Persian'),blank=True, null=True, max_length=250,)
	sub_title_en = models.CharField(_('Sub Title English'),blank=True, null=True, max_length=250,)
	"""
	description persian and english
	"""
	description_fa = models.TextField(_('Description Persian'), blank=False, null=False)
	description_en = models.TextField(_('Description English'), blank=False, null=False)
	
	image_fa = models.ImageField(_('Images Persian'), upload_to='images/', blank=True, null=True)
	image_en = models.ImageField(_('Images English'), upload_to='images/', blank=True, null=True)
	
	created = models.DateTimeField(_('Date Created'),auto_now_add=True)
	status = models.BooleanField(_('Status'), default=True)
	positions = models.IntegerField(_('Position'),choices=list(zip(range(1, 1000), range(1, 1000))), unique=True)

	rtl_or_ltr = models.CharField(_('Direction'), max_length=10, choices=RTLORLTR, blank=False,null=False, default='ltr')
	
	"""
	Button  fields
	"""
	link_name_fa = models.CharField(_('Button name Persian'), max_length=100, default='click me', blank=True, null=True)
	link_name_en = models.CharField(_('Button name English'), max_length=100, default='click me', blank=True, null=True)
	link = models.CharField(_('Button link'), max_length=500, default='#', blank=True, null=True)



	_metadata = {
		'use_title_tag':'true',
		'title': 'get_meta_title',
		'description': 'get_meta_description',
		'image': 'get_meta_image',
		'use_og':'true',
		'use_twitter':'true',
		'get_domain':'hamed-biglari.ir',
	}
	
	def get_meta_title(self):
		lang = get_language()
		return self.title_fa if lang == 'fa' else self.title_en

	def get_meta_description(self):
		lang = get_language()
		raw_html = self.description_fa if lang == 'fa' else self.description_en
		plain_text = strip_tags(raw_html)
		return Truncator(plain_text).chars(160, truncate='...')

	def get_meta_image(self):
		lang = get_language()
		image = self.image_fa if lang == 'fa' else self.image_en
		return image.url if image else None
			


	class Meta:
		ordering = ('positions',)
		verbose_name = _('Part')
		verbose_name_plural = _('Parts')

	def __str__(self):
		return self.part_name_en



	objects = PartManager()


class Contact(models.Model):
	full_name = models.CharField(_('Full Name'), max_length=300, blank=False, null=False)
	email = models.CharField(_('Email'), max_length=500, blank=False, null=False)
	massages = models.TextField(_('Massages'), blank=False, null=False, max_length=500)
	created = models.DateTimeField(_('Date Created'), auto_now_add=True)

	class Meta:
		ordering = ('-created',)
		verbose_name = _('Contact')
		verbose_name_plural = _('Contacts')

	def __str__(self):
		return self.full_name
