import datetime
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
from ta_device.models import (TADevice)
from .forms import (TADeviceForm)
from base.helpers.func import (Breadcrumb, format_search_string, get_fields)


class DeviceCreateView(generic.CreateView):
    model = TADevice
    form_class = TADeviceForm
    template_name = 'partials/forms/form.html'
    success_message = "Device Added Successfully."
    title = 'Add New Time Attendance Device Form'
    success_url = "device_all_list"
    
    def form_valid(self, form, *args, **kwargs):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
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
        return context


class DeviceUpdateView(generic.UpdateView):
    model = TADevice
    form_class = TADeviceForm
    template_name = 'partials/forms/form.html'
    success_message = "Device Update Successfully."
    title = 'Update Time Attendance Device Form'
    success_url = "device_all_list"
    context_object_name = 'instance'


    def form_valid(self, form, *args, **kwargs):
        self.object = form.save(commit=False)
        self.object.updated_by = self.request.user
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
        return context


class DeviceListView(generic.ListView):
    model = TADevice
    context_object_name = 'items'
    template_name = 'device/list.html'
    title = "All Time Attendance Device List"
    queryset = TADevice.objects.all()
    paginate_by = 10
    search_fields = ['ip_address']
    list_display = ['device_name', 'ip_address', 'device_status']
    action_urls = ['device_update', ]  # url_delete, url_update, url_details and item_sublist
    
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
        context['device_count'] = self.get_queryset().count()
        context['title'] = self.title
        # create_url and history_url for right side navigation button.
        context['create_url'] = 'device_create'
        # context['history_url'] = 'device_create'
        breadcrumbs = [
            Breadcrumb(name='Dashboard', url='/'),
            Breadcrumb(name='List'),
        ]
        context['breadcrumbs'] = breadcrumbs
        context['fields'] = get_fields(self.model, self.list_display)
        context['action_urls'] = self.action_urls
        return context