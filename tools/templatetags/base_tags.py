from django import template
from tools.models import Clients,Social,ContactInfo
from resume.models import Part
import re
register = template.Library()



@register.inclusion_tag("resume/tags/clinets.html")
def clinets():
	return {
		"clinets": Clients.objects.active().order_by('-id')
	}

@register.inclusion_tag("resume/tags/social.html")
def socials():
	return {
		"socials": Social.objects.all()
	}

@register.inclusion_tag("resume/tags/contactinfo.html")
def contactinfo():
	return {
		"contactinfo": ContactInfo.objects.all().last()
	}


def menu_item():
	items_list = Part.objects.active().only('part_name_fa', 'part_name_en')
	return items_list 

@register.inclusion_tag("resume/tags/header.html")
def header(request):
	return {'items_list':menu_item(),"request":request}



@register.inclusion_tag("resume/tags/footer.html")
def footer(request):
	return {'items_list':menu_item(),"request":request}



@register.filter
def remove_empty_p(html):
    return re.sub(r'<p>([\s\u200c\u200e\u200f]|&nbsp;)*<\/p>', '', html)