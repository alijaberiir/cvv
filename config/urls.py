"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from resume.views import Change_lang
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import set_language
from blog.sitemaps import PostSitemap
from django.contrib.sitemaps.views import sitemap
from resume.sitemaps import PageSitemap
sitemaps = {
    'blog': PostSitemap,
    'page':PageSitemap
}
from .robots import robots_txt



urlpatterns = [
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path('robots.txt',robots_txt,name='robots_txt'),
    path('tinymce/', include('tinymce.urls')),
    path('change_lang', Change_lang, name='change_lang'),
    path('i18n/setlang/', set_language, name='set_language'),
    
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('',include('resume.urls'),name='resume'),
    path('blog/',include('blog.urls'),name='blog_app'),
    prefix_default_language=False,
    
)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'tools.views.error_404'
handler403 = 'tools.views.error_403'
handler400 = 'tools.views.error_400'

