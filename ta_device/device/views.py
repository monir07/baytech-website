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
from base.helpers.func import (Breadcrumb, format_search_string)


class DeviceCreateView(generic.CreateView):
    model = TADevice
    form_class = TADeviceForm
    template_name = 'partials/forms/form.html'
    success_message = "Device Added Successfully."
    title = 'Add New Device Form'
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
        return context


class DeviceUpdateView(generic.UpdateView):
    model = TADevice
    form_class = TADeviceForm
    template_name = 'partials/forms/form.html'
    success_message = "Device Update Successfully."
    title = 'Update Device Form'
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
        return context


class DeviceListView(generic.ListView):
    model = TADevice
    context_object_name = 'items'
    template_name = 'device/list.html'
    title = "All Device List"
    queryset = TADevice.objects.all()
    paginate_by = 10
    search_fields = ['ip_address']
    
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
        # context['create_url'] = 'notice_create'
        # context['update_url'] = 'notice_app_update'
        # context['delete_url'] = 'notice_app_delete'
        # context['details_url'] = 'notice_app_detail_view'
        return context