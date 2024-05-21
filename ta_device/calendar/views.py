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
from ta_device.models import (Holiday, HolidayCalender)
from .forms import (HolidayForm, HolidayCalenderForm)
from base.helpers.func import (Breadcrumb, format_search_string, get_fields)


class HolidayCreateView(generic.CreateView):
    model = Holiday
    form_class = HolidayForm
    template_name = 'partials/forms/form.html'
    success_message = "Holiday Added Successfully."
    title = 'Add New Holiday Form'
    success_url = "all_holiday_list"
    
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
        context['list_url'] = 'all_holiday_list'
        return context


class HolidayUpdateView(generic.UpdateView):
    model = Holiday
    form_class = HolidayForm
    template_name = 'partials/forms/form.html'
    success_message = "Holiday Update Successfully."
    title = 'Update Holiday Form'
    success_url = "all_holiday_list"
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
        context['list_url'] = 'all_holiday_list'
        return context


class HolidayListView(generic.ListView):
    model = Holiday
    context_object_name = 'items'
    template_name = 'partials/datatable/base-list.html'
    title = "All Holyday List"
    queryset = Holiday.objects.all()
    paginate_by = 10
    search_fields = ['name',]
    list_display = ['name',]
    action_urls = ['holiday_update', ]  # url_delete, url_update, url_details and item_sublist
    
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
        context['create_url'] = 'holiday_create'
        # context['history_url'] = 'device_create'
        breadcrumbs = [
            Breadcrumb(name='Dashboard', url='/'),
            Breadcrumb(name='List'),
        ]
        context['breadcrumbs'] = breadcrumbs
        context['fields'] = get_fields(self.model, self.list_display)
        context['action_urls'] = self.action_urls
        return context


# DEPARTMENT START FROM HERE 

class HolidayCalendarCreateView(generic.CreateView):
    model = HolidayCalender
    form_class = HolidayCalenderForm
    template_name = 'partials/forms/form.html'
    success_message = "holiday calender Added Successfully."
    title = 'Add New Holiday Calendar Form'
    success_url = "all_calendar_list"
    
    def form_valid(self, form, *args, **kwargs):
        self.object = form.save(commit=False)
        date_from = form.cleaned_data['date_from']
        date_to = form.cleaned_data['date_to']
        duration = date_to - date_from
        self.object.total_day = duration.days + 1
        self.object.year = date_from.year
        self.object.save()
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
        context['list_url'] = 'all_calendar_list'
        return context


class HolidayCalendarUpdateView(generic.UpdateView):
    model = HolidayCalender
    form_class = HolidayCalenderForm
    template_name = 'partials/forms/form.html'
    success_message = "Calendar Update Successfully."
    title = 'Update Holiday Calendar Form'
    success_url = "all_calendar_list"
    context_object_name = 'instance'


    def form_valid(self, form, *args, **kwargs):
        self.object = form.save(commit=False)
        date_from = form.cleaned_data['date_from']
        date_to = form.cleaned_data['date_to']
        duration = date_to - date_from
        self.object.total_day = duration.days + 1
        self.object.year = date_from.year
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
        context['list_url'] = 'all_calendar_list'
        return context


class HolidayCalendarListView(generic.ListView):
    model = HolidayCalender
    context_object_name = 'items'
    template_name = 'partials/datatable/base-list.html'
    title = "All Calendar List"
    queryset = HolidayCalender.objects.all()
    paginate_by = 10
    search_fields = ['name', 'holiday_list__name']
    list_display = ['holiday_list', 'date_from', 'date_to', 'total_day', 'year']
    action_urls = ['calendar_update', ]  # url_delete, url_update, url_details and item_sublist
    
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
        context['create_url'] = 'calendar_create'
        # context['history_url'] = 'device_create'
        breadcrumbs = [
            Breadcrumb(name='Dashboard', url='/'),
            Breadcrumb(name='List'),
        ]
        context['breadcrumbs'] = breadcrumbs
        context['fields'] = get_fields(self.model, self.list_display)
        context['action_urls'] = self.action_urls
        return context