from django.contrib.sitemaps import Sitemap
from django.urls import reverse



class PageSitemap(Sitemap):
	changefreq = "monthly"
	priority = 0.8
	protocol = 'https'
	i18n = True
	languages = ['en','fa']
	alternates = True
	x_default = True

	def items(self):
		return [
			'resume:index',
		]
	
	def location(self, item):
		return reverse(item)