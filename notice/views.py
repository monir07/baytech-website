from django.db import transaction
from django.db.models import ProtectedError, Q
from django.shortcuts import get_object_or_404, render, HttpResponseRedirect
from django.views import generic
from django.urls import reverse_lazy
from django.http.response import HttpResponseRedirect
from django.contrib import messages
from django.utils import timezone
from base.helpers.func import format_search_string
from base.mixins import CommonMixin
from .models import Notice, Noc


# Notice List Start From views here.
class NoticePublishListView(generic.ListView):
    model = Notice
    paginate_by = '10'
    context_object_name = 'items'
    template_name = 'pages/noitce-list.html'
    title = "Notice Draft List"
    queryset = Notice.objects.all()
    search_fields = ['publish_date']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(Q(initial_sign__isnull=False))

        query_param = self.request.GET.copy()
        search_param = query_param.get('query', None)
        if search_param:
            Qr = format_search_string(self.search_fields, search_param)
            queryset = queryset.filter(Qr)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notice_count'] = self.queryset
        context['details_url'] = 'notice_app_detail_view'
        return context


class NoticeDetailView(generic.DetailView):
    model = Notice
    context_object_name = 'item'
    pk_url_kwarg = 'pk'
    template_name = 'pages/notice-details.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# Notice List Start From views here.
class NocPublishListView(generic.ListView):
    model = Noc
    paginate_by = '10'
    context_object_name = 'items'
    template_name = 'pages/noc_list.html'
    queryset = Noc.objects.all()
    search_fields = ['publish_date']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(Q())

        query_param = self.request.GET.copy()
        search_param = query_param.get('query', None)
        if search_param:
            Qr = format_search_string(self.search_fields, search_param)
            queryset = queryset.filter(Qr)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notice_count'] = self.queryset
        return context


class NocDetailView(generic.DetailView):
    model = Notice
    context_object_name = 'item'
    pk_url_kwarg = 'pk'
    template_name = 'pages/notice-details.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
