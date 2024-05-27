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
from ta_device.models import (Attendance)
from .forms import (AttendanceForm)
from base.helpers.func import (Breadcrumb, format_search_string, get_fields)


class AttendanceCreateView(generic.CreateView):
    model = Attendance
    form_class = AttendanceForm
    template_name = 'partials/forms/form.html'
    success_message = "Attendance Added Successfully."
    title = 'Add New Attendance Form'
    success_url = "all_attendance_list"
    
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
        context['list_url'] = 'all_attendance_list'
        return context


class AttendanceUpdateView(generic.UpdateView):
    model = Attendance
    form_class = AttendanceForm
    template_name = 'partials/forms/form.html'
    success_message = "Attendance Update Successfully."
    title = 'Update Attendance Form'
    success_url = "all_attendance_list"
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
        context['list_url'] = 'all_attendance_list'
        return context


class AttendanceListView(generic.ListView):
    model = Attendance
    context_object_name = 'items'
    template_name = 'attendance/daily_list.html'
    title = "All Attendance List"
    queryset = Attendance.objects.all()
    paginate_by = 10
    search_fields = ['emp__emp_id_no', 'punch_in_device__ip_address', 'punch_out_device__ip_address']
    list_display = ['emp', 'punch_in_device', 'punch_in_date', 'punch_in_time', 
                'punch_out_device', 'punch_out_date', 'punch_out_time', 'status']
    action_urls = ['attendance_update', ]  # url_delete, url_update, url_details and item_sublist
    
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
        context['create_url'] = 'attendance_create'
        # context['history_url'] = 'device_create'
        breadcrumbs = [
            Breadcrumb(name='Dashboard', url='/'),
            Breadcrumb(name='List'),
        ]
        context['breadcrumbs'] = breadcrumbs
        context['fields'] = get_fields(self.model, self.list_display)
        context['action_urls'] = self.action_urls
        return context