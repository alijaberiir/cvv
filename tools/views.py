
from django.shortcuts import render
# Create your views here.
import random
from django.utils.safestring import mark_safe
import json
from django.utils.translation import gettext_lazy as _
from blog.models import Post,comments
from resume.models import Contact,Part
from hitcount.models import HitCount,Hit
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models.functions import TruncDay
from django.db.models import Count
import json


def error_404(request, exception):
	data = {}
	return render(request,'resume/404.html',data)


def error_403(request, exception):
	data = {}
	return render(request,'resume/403.html',data)

def error_400(request, exception):
	data = {}
	return render(request,'resume/400.html',data)

# def error_500(request, exception):
# 	data = {}
# 	return render(request,'resume/500.html',data)


def dashboard_callback(request, context):
	
	post_total = Post.objects.filter(status='published').count
	contactus= Contact.objects.all()
	comments_total = comments.objects.all().count
	part_total = Part.objects.all().count
	

	post_content_type = ContentType.objects.get_for_model(Post)
	hitcounts = HitCount.objects.filter(content_type=post_content_type)
	total_hits = sum(hc.hits for hc in hitcounts)

	now = timezone.now()
	start_date = now - timezone.timedelta(days=27)

	daily_hits = (
		Hit.objects.filter(hitcount__in=hitcounts, created__gte=start_date)
		.annotate(day=TruncDay("created"))
		.values("day")
		.annotate(count=Count("id"))
		.order_by("day")
	)
	labels = []
	data = []
	hit_map = {entry["day"].date(): entry["count"] for entry in daily_hits}

	for i in range(27):
		day = (start_date + timezone.timedelta(days=i)).date()
		labels.append(day.strftime("%b %d"))  
		data.append(hit_map.get(day, 0))
			
	chart_data = {
		"labels": labels,
		"datasets": [{
			"data": data,
			"borderColor": "#9333ea"
		}]
	}

	context.update(
		{ 
			"kpi": [
				{
					"title": _("All Blogs Published"),
					"metric": post_total,
					
				},
				{
					"title": _("All Messages"),
					"metric": contactus.count,
					
				},
				{
					"title": _("All Comments"),
					"metric": comments_total,
					
				},
				{
					"title": _("All Parts"),
					"metric": part_total,
					
				},
				{
					"title": _("All Visit"),
					"metric": total_hits,
				},
			],
	
			"performance": [
				{
					"title": _("Blog Visit"),
					"chart": json.dumps(chart_data),
				}
			],
			"contactus":contactus
		},
	)

	return context