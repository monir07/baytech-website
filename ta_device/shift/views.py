from datetime import datetime, date, timedelta
from django.db import transaction
from django.db.models import Q, Prefetch, Sum, Value
from django.shortcuts import get_object_or_404, render, HttpResponseRedirect
from django.views import generic
from django.urls import reverse_lazy
from django.http.response import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.template import loader
from django.http import HttpResponse
from ta_device.models import (Shift)
from .forms import (ShiftForm)
from base.helpers.func import (Breadcrumb, format_search_string, get_fields, get_duration)


class ShiftCreateView(generic.CreateView):
    model = Shift
    form_class = ShiftForm
    template_name = 'partials/forms/form.html'
    success_message = "Shift Added Successfully."
    title = 'Add New Shift Form'
    success_url = "all_shift_list"
    
    def form_valid(self, form, *args, **kwargs):
        self.object = form.save(commit=False)
        start_time = form.cleaned_data['start_time']
        end_time = form.cleaned_data['end_time']
        duration = get_duration(start_time, end_time)
        self.object.shift_duration = str(duration)
        with transaction.atomic():
            form.save()
        messages.success(self.request, self.success_message)
        return self.get_success_url()

    def get_success_url(self) -> str:
        return HttpResponseRedirect(reverse_lazy(self.success_url))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        breadcrumbs = [
            Breadcrumb(name='Dashboard', url='/'),
            Breadcrumb(name='Create'),
        ]
        context['breadcrumbs'] = breadcrumbs
        context['list_url'] = 'all_shift_list'
        return context
    


class ShiftUpdateView(generic.UpdateView):
    model = Shift
    form_class = ShiftForm
    template_name = 'partials/forms/form.html'
    success_message = "Shift Update Successfully."
    title = 'Update Shift Form'
    success_url = "all_shift_list"
    context_object_name = 'instance'


    def form_valid(self, form, *args, **kwargs):
        self.object = form.save(commit=False)
        start_time = form.cleaned_data['start_time']
        end_time = form.cleaned_data['end_time']
        duration = get_duration(start_time, end_time)
        self.object.shift_duration = str(duration)
        self.object.save()
        messages.success(self.request, self.success_message)
        return self.get_success_url()

    def get_success_url(self) -> str:
        return HttpResponseRedirect(reverse_lazy(self.success_url))


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        breadcrumbs = [
            Breadcrumb(name='Dashboard', url='/'),
            Breadcrumb(name='Update'),
        ]
        context['breadcrumbs'] = breadcrumbs
        context['list_url'] = 'all_shift_list'
        return context


class ShiftListView(generic.ListView):
    model = Shift
    context_object_name = 'items'
    template_name = 'device/shift_list.html'
    title = "All Shift List"
    queryset = Shift.objects.all()
    paginate_by = 10
    search_fields = ['name', ]
    list_display = ['name', 'start_time', 'end_time', 'shift_duration', 'sat', 'sun', 'mon', 'tue', 'wed', 'thu', 'fri']
    action_urls = ['shift_update', ]  # url_delete, url_update, url_details and item_sublist
    
    def get_queryset(self):
        queryset = super().get_queryset()

        query_param = self.request.GET.copy()
        search_param = query_param.get('query', None)
        if search_param:
            Qr = format_search_string(self.search_fields, search_param)
            queryset = queryset.filter(Qr)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query_count'] = self.get_queryset().count()
        context['title'] = self.title
        # create_url and history_url for right side navigation button.
        context['create_url'] = 'shift_create'
        # context['history_url'] = 'device_create'
        breadcrumbs = [
            Breadcrumb(name='Dashboard', url='/'),
            Breadcrumb(name='List'),
        ]
        context['breadcrumbs'] = breadcrumbs
        context['fields'] = get_fields(self.model, self.list_display)
        context['action_urls'] = self.action_urls
        return context