from django.views import generic
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.http.response import HttpResponseRedirect
from django.views.generic.edit import FormMixin
from base.helpers.func import (format_search_string, generate_qr_code)
from django.db.models import Q
from page.models import (Project, ProjectInformation, ProjectMachinery, 
                         ProjectTypeChoices, ProjectCategoryChoices, 
                         NewsInsight, JobPost, ContactUs, DockingCertificate)
from page.forms import (ContactUsForm, DockingCertificateSearchForm)

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



class DockingCertificateSearchView(FormMixin, generic.View):
    title = "Docking Certificate Search Form"
    form_class = DockingCertificateSearchForm
    template_name = 'pages/search_form.html'
    

    def get(self, request, *args, **kwargs):
        if '_docking_search' in self.request.GET:
            form_class = self.get_form_class()
            form = form_class(self.request.GET)
            if form.is_valid():
                form_data = form.cleaned_data
                certificate_no = form_data.get('certificate_no', None)

                query = Q()
                if certificate_no:
                    query = query & Q(certificate_no=certificate_no)
                
                try:
                    query_object = DockingCertificate.objects.get(query)
                except DockingCertificate.DoesNotExist:
                    messages.warning(self.request, f'Docking Certificate: {certificate_no} Not Found!!')
                    return redirect('docking_certificate_search')
                

                self.template_name = 'pages/docking_certificate.html'
                certificate_url = f"http://127.0.0.1:8000/docking-certificate/details/{query_object.certificate_no}"

                # Generate QR code
                qr_code_image = generate_qr_code(certificate_url)                

                context = {
                    'item' : query_object,
                    'qr_code_image' : qr_code_image,
                    'certificate_url': certificate_url
                }
                return render(request, self.template_name, context)
        else:
            form = self.get_form()
            context = {
                'form': form,
                'title': self.title,
                }
            return render(request, self.template_name, context)


class DockingCertificateDetailView(generic.DetailView):
    model = DockingCertificate
    context_object_name = 'item'
    slug_field = 'certificate_no'  # Field to use for lookup
    slug_url_kwarg = 'certificate_no'  # URL keyword argument
    template_name = 'pages/docking_certificate.html'


    # Optional: Override get_object if you need custom logic
    def get_object(self, queryset=None):
        # Get the certificate_no from the URL
        certificate_no = self.kwargs.get('certificate_no')
        # Fetch the object using the certificate_no
        return get_object_or_404(DockingCertificate, certificate_no=certificate_no)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        certificate_object = self.get_object()
        certificate_url = f"http://127.0.0.1:8000/docking-certificate/details/{certificate_object.certificate_no}/"
        # Generate QR code
        qr_code_image = generate_qr_code(certificate_url)
        context['qr_code_image'] = qr_code_image 
        return context