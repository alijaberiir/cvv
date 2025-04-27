from django.views.generic import ListView
from hitcount.views import HitCountDetailView
from .models import Post
from django.utils import timezone
from .forms import comments_form
from django.views.generic import View
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.contrib import messages


class PostListView(ListView):
	model = Post
	template_name = 'blog/post_list.html'
	context_object_name = 'posts'
	paginate_by = 12

	def get_queryset(self):
		queryset = Post.objects.filter(status='published',published__lte=timezone.now())
		return queryset
	


class PostDetailView(HitCountDetailView):
	model = Post
	template_name = 'blog/post_detail.html'
	context_object_name = 'post'
	count_hit = True


	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		post = self.get_object()
		context['meta'] = post.as_meta(self.request)
		related_posts = Post.objects.filter(status='published',published__lte=timezone.now()).exclude(id=post.id).distinct()[:3]
		context['related_posts'] = related_posts
		context['form'] = comments_form()
		return context




class CommentView(View):
	def post(self, request, *args, **kwargs):
		blog_id = request.POST.get('blog_id')
		form = comments_form(request.POST, blog_id=blog_id)
		if form.is_valid():
			form.save() 		
			messages.success(request, _('Thanks! Your comment was sent successfully.'))
		else:
			messages.error(request, _('Sorry, your message was not sent. Please try again.'))

		return redirect(request.META.get('HTTP_REFERER', '/'))