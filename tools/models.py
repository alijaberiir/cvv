from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from .utils import SELECT_ICONS
from django.utils.safestring import mark_safe


class SocialManager(models.Manager):
	def active(self):
		return self.filter(status = True)

class ClinetManager(models.Manager):
	def active(self):
		return self.filter(status = True)





class Clients(models.Model):
	name_en = models.CharField(_('Name English'),default='clinet', max_length=200, blank=False, null=False)
	link = models.CharField(_('site link'), max_length=500, default='#', blank=True, null=True)
	image = models.ImageField(_('Images'), upload_to='images/', blank=False, null=False)
	status = models.BooleanField(_('Status'), default=True)

	class Meta:
		ordering = ('name_en',)
		verbose_name = _('Clinet & Work')
		verbose_name_plural = _('Clinets & Works')

	def __str__(self):
		return self.name_en

	objects =ClinetManager()


class Social(models.Model):
	icon = models.CharField(_('icon'), max_length=200, blank=True, null=True, choices=SELECT_ICONS)
	link = models.CharField(_('link'), max_length=500, default='#', blank=True, null=True,help_text="https://youraddress or http://youraddress")
	status = models.BooleanField(_('Status'), default=True)

	class Meta:
		ordering = ('link',)
		verbose_name = _('Social')
		verbose_name_plural = _('Social')

	def __str__(self):
		return self.link

	def icon_svg(self):
		if self.icon:
			return mark_safe(self.get_icon_display())



class ContactInfo(models.Model):
	phone = models.CharField(_('Phone'), max_length=15, blank=False, null=False)
	email = models.EmailField(_('Email'), blank=False, null=False)
	address_fa = models.TextField(_('Address Persian'), blank=False, null=False, max_length=500)
	address_en = models.TextField(_('Address English'), blank=False, null=False, max_length=500)

	class Meta:
		ordering = ('phone',)
		verbose_name = _('Contact Info')
		verbose_name_plural = _('Contacts Info')

	def __str__(self):
		return self.phone


class Dashboard(models.Model):
	title = models.CharField(max_length=150,blank=True,null=True)