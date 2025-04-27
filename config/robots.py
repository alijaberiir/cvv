from django.http import HttpResponse
from django.views.decorators.http import require_GET

@require_GET
def robots_txt(request):
    return HttpResponse(robots_txt_content, content_type="text/plain")


robots_txt_content = """\
User-agent: *
Disallow: /admin/*
Disallow: /ratings/*
Disallow: /tinymce/*
Disallow: /change_lang/*
Disallow: /i18n/*
Disallow: /blog/comment/*
Disallow: /NewContact/*
Sitemap: https://hamed-biglari.ir/sitemap.xml
"""