from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.

class TemplatePageView(TemplateView):
    template_name = "home.html"
    image_urls = ['', '', '']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image_urls'] = self.image_urls
        return context
