from django.views import generic
from django.urls import reverse_lazy
from django.contrib import messages
from django.http.response import HttpResponseRedirect
from base.helpers.func import format_search_string
from django.db.models import Q
from page.models import (Project, ProjectInformation, ProjectMachinery, 
                         ProjectTypeChoices, ProjectCategoryChoices, 
                         NewsInsight, JobPost, ContactUs)
from page.forms import (ContactUsForm,)

class TemplatePageView(generic.TemplateView):
    template_name = "home.html"
    image_urls = ['', '', '']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image_urls'] = self.image_urls
        return context


# PROJECT List Start From views here.
class NewBuildingProjectListView(generic.ListView):
    model = Project
    paginate_by = '4'
    context_object_name = 'items'
    template_name = 'pages/project_list.html'
    queryset = Project.objects.filter()
    search_fields = ['proejct_no']
    title = 'On Going New Building Project'
    

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(Q(proejct_type=ProjectTypeChoices.NEW, 
                                    proejct_category=ProjectCategoryChoices.ONGOING))

        query_param = self.request.GET.copy()
        search_param = query_param.get('query', None)
        if search_param:
            Qr = format_search_string(self.search_fields, search_param)
            queryset = queryset.filter(Qr)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query_count'] = self.get_queryset
        context['title'] = self.title
        return context


class RepairProjectListView(generic.ListView):
    model = Project
    paginate_by = '10'
    context_object_name = 'items'
    template_name = 'pages/project_list.html'
    queryset = Project.objects.filter()
    search_fields = ['proejct_no']
    title = 'On Going Repair Project'
    

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(Q(proejct_type=ProjectTypeChoices.REPAIR, 
                                    proejct_category=ProjectCategoryChoices.ONGOING))

        query_param = self.request.GET.copy()
        search_param = query_param.get('query', None)
        if search_param:
            Qr = format_search_string(self.search_fields, search_param)
            queryset = queryset.filter(Qr)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query_count'] = self.get_queryset
        context['title'] = self.title
        return context


class CompletedProjectListView(generic.ListView):
    model = Project
    paginate_by = '10'
    context_object_name = 'items'
    template_name = 'pages/project_list.html'
    queryset = Project.objects.filter()
    search_fields = ['proejct_no']
    title = 'Completed Project'
    

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(Q(proejct_category=ProjectCategoryChoices.COMPLETED))

        query_param = self.request.GET.copy()
        search_param = query_param.get('query', None)
        if search_param:
            Qr = format_search_string(self.search_fields, search_param)
            queryset = queryset.filter(Qr)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query_count'] = self.queryset.count()
        context['title'] = self.title
        return context
    

class ProjectDetailView(generic.DetailView):
    model = Project
    context_object_name = 'item'
    pk_url_kwarg = 'pk'
    template_name = 'pages/project_details.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context



# NEWS AND INSIGHT PAGES START FROM HERE
class NewsInsightListView(generic.ListView):
    model = NewsInsight
    paginate_by = '10'
    context_object_name = 'items'
    template_name = 'pages/news_list.html'
    queryset = NewsInsight.objects.filter()
    search_fields = ['proejct_no']
    title = 'News & Insights'
    

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
        context['query_count'] = self.queryset.count()
        context['title'] = self.title
        return context


class NewsDetailView(generic.DetailView):
    model = NewsInsight
    context_object_name = 'item'
    pk_url_kwarg = 'pk'
    template_name = 'pages/news_details.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# JOB POST PAGES START FROM HERE
class JobPostListView(generic.ListView):
    model = JobPost
    paginate_by = '10'
    context_object_name = 'items'
    template_name = 'pages/job-post-list.html'
    queryset = JobPost.objects.filter()
    search_fields = ['proejct_no']
    title = 'Empower Your Career Journey with Us'
    

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(Q(is_active=True))

        query_param = self.request.GET.copy()
        search_param = query_param.get('query', None)
        if search_param:
            Qr = format_search_string(self.search_fields, search_param)
            queryset = queryset.filter(Qr)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query_count'] = self.get_queryset()
        context['title'] = self.title
        return context


# CONTACT US START FORM HERE
class ContactUsCreateView(generic.CreateView):
    form_class = ContactUsForm
    model = ContactUs
    template_name = 'pages/contact_us.html'
    success_message = 'message send successfully'
    success_url = reverse_lazy("contact_us_create")


    def form_valid(self, form, *args, **kwargs):
        self.object = form.save(commit=False)
        self.object.save()
        messages.success(self.request, self.success_message)
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context