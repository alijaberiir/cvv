from django.contrib import admin
from django.utils.html import format_html
from .models import Post,comments
from unfold.admin import ModelAdmin
from tinymce.widgets import TinyMCE
from django.db import models
from .models import Post
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import truncatechars
from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext_lazy as _

from hitcount.models import Hit, BlacklistIP, BlacklistUserAgent
from hitcount.utils import get_hitcount_model
from unfold.admin import ModelAdmin

        
@admin.register(Post)
class PostAdmin(ModelAdmin):
    fieldsets = (
		(_("Persian"), {
			"classes": ["tab"],
			"fields": ["title","content"]
		}),
		(_("English"), {
			"classes": ["tab"],
			"fields": ["title_en","slug","content_en"],
		}),
		(_("General"), {
			"classes": ["tab"],
			"fields": ["featured_image","status","published"],
		}),
	)

    list_display = ['featured_image_display','get_hit_count', 'status', 'published','updated']
    list_filter = ['status', 'created', 'published']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title_en',)}
    date_hierarchy = 'published'
    ordering = ['-published', '-created']
    readonly_fields = ['created', 'updated']
    formfield_overrides = {
		models.TextField: {'widget': TinyMCE()},
	}
    

    def get_hit_count(self, obj):
        return obj.hit_count.hits
    get_hit_count.short_description = _("Visits")

    def featured_image_display(self, obj):
        if obj.featured_image:
            return format_html(f'<div class="blog-list"><img src="{obj.featured_image.url}"><span><strong>{truncatechars(obj.title,30)}</strong><strong>{truncatechars(obj.title_en,30)}</strong</span></div>')
        return format_html(f'<span><strong>{truncatechars(obj.title,30)}</strong><strong>{truncatechars(obj.title_en,30)}</strong</span>')
    featured_image_display.short_description = _("blog")



    
@admin.register(comments)
class CommentsAdmin(ModelAdmin):
    list_display = ['full_name','email', 'status', 'created']
    list_filter = ['status', 'created']
    search_fields = ['full_name', 'email','comments']
    fields = ['full_name','email', 'comments', 'status']
    ordering = ['-created',]
    readonly_fields = ['created',]
   
 
