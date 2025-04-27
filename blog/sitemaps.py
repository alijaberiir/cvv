from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Post



class PostSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5
    protocol = 'https'
    i18n = True
    languages = ['en','fa']
    alternates = True
    x_default = True

    def items(self):
        return Post.objects.published()

    def lastmod(self, obj):
        return obj.published

    def location(self, item):
        return reverse('blog:post_detail', kwargs={'slug': item.slug})
    