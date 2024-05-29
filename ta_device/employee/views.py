import datetime
from django.db import transaction
from django.db.models import Q, Prefetch, Sum, Value
from django.shortcuts import get_object_or_404, render, HttpResponseRedirect
from django.views import generic
from django.urls import reverse_lazy
from django.http.response import HttpResponseRedirect, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.template import loader
from django.http import HttpResponse
from ta_device.models import (Employee)
from .forms import (EmployeeForm)
from base.helpers.func import (Breadcrumb, format_search_string, get_fields)
from base.helpers.utils import (identifier_builder)
from zk import ZK, const


class EmployeeCreateView(LoginRequiredMixin, generic.CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'partials/forms/form.html'
    success_message = "Employee Added Successfully."
    title = 'Add New Employee Form'
    success_url = "all_employee_list"
    
    def form_valid(self, form, *args, **kwargs):
        self.object = form.save(commit=False)
        device_obj = form.cleaned_data['device']
        name = form.cleaned_data['name']
        device_id_no = form.cleaned_data['device_id_no']
        card_no = form.cleaned_data['card_no']
        self.object.created_by = self.request.user
        zk = ZK(device_obj.ip_address, port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)
        
        try:
            # connect to device
            conn = zk.connect()
            # print ("Conncection Success.")
            # enable device
            conn.enable_device()
            # print ("Device Enable.")
            # Create user
            id_no = int(identifier_builder(table_name='ta_device_employee'))
            # print('Device UID', id_no)
            conn.set_user(uid=id_no, name=name, privilege=const.USER_DEFAULT, password='12345678', group_id='', user_id=str(device_id_no), card=card_no)
            form.save()
            messages.success(self.request, self.success_message)
            return self.get_success_url()
        except Exception as e:
            print ("Process terminate : {}".format(e))
            messages.error(self.request, f'Process terminate: {e}')
            return self.form_invalid(form)

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
        context['list_url'] = 'all_employee_list'
        return context


class EmployeeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'partials/forms/form.html'
    success_message = "Employee Update Successfully."
    title = 'Update Employee Form'
    success_url = "all_employee_list"
    context_object_name = 'instance'


    def form_valid(self, form, *args, **kwargs):
        self.object = form.save(commit=False)
        self.object.updated_by = self.request.user
        device_obj = form.cleaned_data['device']
        name = form.cleaned_data['name']
        device_id_no = form.cleaned_data['device_id_no']
        card_no = form.cleaned_data['card_no']
        zk = ZK(device_obj.ip_address, port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)
        try:
            # connect to device
            conn = zk.connect()
            # print ("Conncection Success.")
            # enable device
            conn.enable_device()
            # print ("Device Enable.")
            u_id = self.get_object()
            print(u_id.pk, 'device uid no')
            conn.set_user(uid=u_id.pk, name=name, privilege=const.USER_DEFAULT, password='12345678', group_id='', user_id=str(device_id_no), card=card_no)
            form.save()
            messages.success(self.request, self.success_message)
            return self.get_success_url()
        except Exception as e:
            print ("Process terminate : {}".format(e))
            messages.error(self.request, f'Process terminate: {e}')
            return self.form_invalid(form)

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
        context['list_url'] = 'all_employee_list'
        return context


class EmployeeListView(LoginRequiredMixin, generic.ListView):
    model = Employee
    context_object_name = 'items'
    template_name = 'partials/datatable/base-list.html'
    title = "All Employee List"
    queryset = Employee.objects.all()
    paginate_by = 10
    search_fields = ['emp_id_no', 'section__name', 'device__ip_address']
    list_display = ['device', 'device_id_no', 'emp_id_no', 'name', 'designation', 'section', 'shift', 'card_no']
    action_urls = ['employee_update', 'employee_delete' ]  # url_delete, url_update, url_details and item_sublist
    
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
        context['create_url'] = 'employee_create'
        # context['history_url'] = 'device_create'
        breadcrumbs = [
            Breadcrumb(name='Dashboard', url='/'),
            Breadcrumb(name='List'),
        ]
        context['breadcrumbs'] = breadcrumbs
        context['fields'] = get_fields(self.model, self.list_display)
        context['action_urls'] = self.action_urls
        return context


class EmployeeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Employee
    template_name = 'components/confirm_delete.html'
    success_url = 'all_employee_list'

    def form_valid(self, form):
        emp_obj = self.object
        zk = ZK(emp_obj.device.ip_address, port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)
        try:
            conn = zk.connect()
            conn.enable_device()
            conn.delete_user(user_id=emp_obj.device_id_no)
            self.object.delete()
            messages.success(self.request, "Deleted Successfully.")
            return HttpResponseRedirect(self.get_success_url())
        except Exception as e:
            messages.warning(self.request, f'{e}')
            return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self, **kwargs):
        return reverse_lazy(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['details'] = self.get_object()._meta.verbose_name
        context['list_url'] = 'all_employee_list'
        context['title'] = 'Confirm Delete'
        breadcrumbs = [
            Breadcrumb(name='Dashboard', url='/'),
            Breadcrumb(name='List', url='/tam/employee/all-list/'),
            Breadcrumb(name='confirm-delete'),
        ]
        context['breadcrumbs'] = breadcrumbs
        return context