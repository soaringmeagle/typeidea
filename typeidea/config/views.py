from django.shortcuts import render
from django.views.generic import ListView
from blog.views import CommonViewMixin
from .models import Link


# Create your views here.

class LinkView(CommonViewMixin, ListView):
    queryset = Link.objects.filter(status=Link.STATUS_NORMAL).order_by('-weight')
    template_name = 'config/links.html'
    context_object_name = 'link_list'
