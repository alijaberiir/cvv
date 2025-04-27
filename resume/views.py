from django.shortcuts import redirect, render
from django.views.generic import ListView,CreateView
from django.utils.translation import activate
from .models import Part
from django.urls import reverse_lazy
from .forms import contact
from django.utils.translation import gettext_lazy as _
from django.contrib import messages




class Index(ListView):
	queryset = Part.objects.active()
	ordering = ['positions']
	template_name = 'resume/index.html'


	def get_context_data(self, **kwargs):
		context = super(Index, self).get_context_data(**kwargs)
		context['form'] = contact()

		first_part = self.get_queryset().first()
		if first_part:
			context['meta'] = first_part.as_meta(self.request)
		return context



def Change_lang(request):
	activate(request.GET.get('lang'))
	return redirect('resume:index')

class NewContact(CreateView):
	form_class = contact
	success_url = reverse_lazy('resume:index')
	template_name = 'resume/index.html'
	
	def get_context_data(self, **kwargs):
		context = super(NewContact, self).get_context_data(**kwargs)
		context['form'] = contact()
		context['object_list']  = Part.objects.active().order_by('positions')
		return context
		
		
	def form_valid(self, form):
		if form.is_valid():
			messages.success(self.request, _('Thanks Your message was sent successfully.'))
			return super(NewContact, self).form_valid(form)
		else:
			messages.error(self.request, _('Sorry, your message was not sent. Please try again.'))
			return super(NewContact, self).form_valid(form)
