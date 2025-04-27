from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation
from django.utils import translation
from django.template import Template, Context
from django.utils.translation import gettext_lazy as _
from meta.models import ModelMeta
from django.utils.translation import get_language
from django.utils.text import Truncator
from django.utils.html import strip_tags
import json
from django.utils.html import escape

User = get_user_model()

class PostManager(models.Manager):
	def published(self):
		return self.filter(status = 'published')
	
class Post(ModelMeta, models.Model, HitCountMixin):
	STATUS_CHOICES = (('draft', _('draft')),('published', _('published')))

	title = models.CharField(_('title'), max_length=200)
	title_en = models.CharField(_('english title'), max_length=200,null=True)

	content = models.TextField(_('content'),null=True)
	content_en = models.TextField(_('english content'),null=True)

	slug = models.SlugField(_('slug'), max_length=200, unique=True, allow_unicode=True)
	
	featured_image = models.ImageField(_('featured_image'),
									 upload_to='blog/images/%Y/%m/%d/',
									 blank=True)

	

	status = models.CharField(_('status'), max_length=10,choices=STATUS_CHOICES, default='draft')

	created = models.DateTimeField(_('created'), auto_now_add=True)
	updated = models.DateTimeField(_('updated'), auto_now=True)
	published = models.DateTimeField(_('published'), null=True, blank=True)
	hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
									  related_query_name='hit_count_generic_relation')
	
	

	_metadata = {
		'use_title_tag':'true',
		'title': 'get_meta_title',
		'description': 'get_meta_description',
		'image': 'get_meta_image',
		'use_og':'true',
		'use_twitter':'true',
		'get_domain':'hamed-biglari.ir',
		'use_schemaorg':'true'
	}


	_schema = {
		'image': 'get_meta_image',
		'articleBody': 'get_content',
		'author': 'Hamed Biglari',
		'copyrightYear': 'copyright_year',
		'dateCreated': 'created',
		'dateModified': 'updated',
		'datePublished': 'published',
		'headline': 'get_meta_title',
		'description': 'get_meta_description',
		'name': 'get_meta_title',
		'url': 'get_absolute_url',
		'mainEntityOfPage': 'get_absolute_url',
		'publisher': 'https://hamed-biglari.ir',
	}
	

	def copyright_year(self):
		return self.created.year if self.created else None

	def get_meta_title(self):
		lang = get_language()
		return self.title if lang == 'fa' else self.title_en
	
	def get_content(self):
		lang = get_language()
		return self.content if lang == 'fa' else self.content_en
	
	
	def get_meta_description(self):
		lang = get_language()
		raw_html = self.content if lang == 'fa' else self.content_en
		plain_text = strip_tags(raw_html)
		return Truncator(plain_text).chars(160, truncate='...')

	def get_meta_image(self):
		image = self.featured_image
		return image.url if image else None
			
	def get_absolute_url(self):
		return reverse('blog:post_detail', kwargs={'slug': self.slug})

	def get_schema_json(self):
		return json.dumps({
			"@context": "https://schema.org",
			"@type": "BlogPosting",
			"mainEntityOfPage": {
				"@type": "WebPage",
				"@id": self.get_absolute_url()
			},
			"headline": self.get_meta_title(),
			"description": self.get_meta_description(),
			"image": self.get_meta_image(),
			"author": {
				"@type": "Person",
				"name": "Hamed Biglari"
			},
			"publisher": {
				"@type": "Organization",
				"name": "Hamed Biglari",
				"logo": {
					"@type": "ImageObject",
					"url": self.get_meta_image()  # یا لوگوی سایت
				}
			},
			"datePublished": self.published.isoformat() if self.published else "",
			"dateModified": self.updated.isoformat() if self.updated else "",
			"articleBody": self.get_content(),
		}, ensure_ascii=False)



	class Meta:
		verbose_name = _('Blog')
		verbose_name_plural = _('Blogs')
		ordering = ['-published']
		indexes = [
			models.Index(fields=['-published']),
			models.Index(fields=['status']),
			models.Index(fields=['slug']),
		]

	def __str__(self):
		lang = translation.get_language()
		if lang == 'en':
			return self.title_en or self.title
		return self.title

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.title_en, allow_unicode=True)
		super().save(*args, **kwargs)



	objects = PostManager()





class comments(models.Model):
	STATUS_CHOICES = (('draft', _('draft')),('allowed', _('Allowed')))

	full_name = models.CharField(_("Full Name"), max_length=50)
	email = models.EmailField(_("Email"), max_length=254)
	comments = models.TextField(_("Comments"),null=True,max_length=300)
	blog_id = models.ForeignKey(Post, on_delete=models.CASCADE,null=True)
	created = models.DateTimeField(_('created'), auto_now_add=True,null=True)
	status = models.CharField(_('status'), max_length=10,choices=STATUS_CHOICES, default='draft',null=True)

	def __str__(self):
		return self.full_name 
	
	class Meta:
		verbose_name = _('Comment')
		verbose_name_plural = _('Comments')
		ordering = ['-created']
		indexes = [
			models.Index(fields=['-created']),
			models.Index(fields=['status']),
			models.Index(fields=['full_name']),
		]