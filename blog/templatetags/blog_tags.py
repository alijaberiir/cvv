from django import template
from blog.models import comments
register = template.Library()



@register.inclusion_tag("blog/tags/comments.html")
def comments_list(id):
	return {
		"comments": comments.objects.filter(blog_id=id,status='allowed')
        }
