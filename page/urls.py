from django.urls import path
from .views import (TemplatePageView, NewBuildingProjectListView, 
                    ProjectDetailView, CompletedProjectListView, RepairProjectListView, 
                    NewsInsightListView, NewsDetailView, JobPostListView, ContactUsCreateView,
                    DockingCertificateSearchView, DockingCertificateDetailView, TeamMemberListView)
from .models import (JobPost, TeamMember)


urlpatterns = [
    path('photo-gallery/', TemplatePageView.as_view(
        template_name = "pages/photo_gallery.html",
    ), name='photo_gallery'),
    # about us urls
    path('about-us/', TemplatePageView.as_view(
        template_name = "pages/about_us.html",
    ), name='about_us'),
    # all business urls
    path('all-businesses/', TemplatePageView.as_view(
        template_name = "pages/business-list.html",
    ), name='all_business_list'),
    path('shipbuilding/', TemplatePageView.as_view(
        template_name = "pages/shipbuilding.html",
        image_urls = ['assets/img/slider/slide19.jpg', 
                      'assets/img/slider/slide16.jpg', 
                      'assets/img/slider/slide17.jpg'],
        banner_texts = ['Ship design', 
                        'Consultancy', 
                        'Shi'],
    ), name='shipbuilding'),

    path('ship-design/', TemplatePageView.as_view(
        template_name = "pages/shipdesign.html",
        image_urls = ['assets/img/slider/design-banner-01.jpg', 
                      'assets/img/slider/design-banner-01.jpg', 
                      'assets/img/slider/slide17.jpg'],
        banner_texts = ['Ship design', 
                        'Consultancy', 
                        'Ship Design & Consultancy'],
    ), name='ship_design'),

    path('ndt-services/', TemplatePageView.as_view(
        template_name = "pages/ndt_engineering.html",
        image_urls = ['assets/img/slider/ndt-banner-01.jpg', 
                      'assets/img/slider/ndt-banner-01.jpg', 
                      'assets/img/slider/slide17.jpg'],
        banner_texts = ['Bay-Tech NDT Services', 
                        'Bay-Tech NDT Services', 
                        'Bay-Tech NDT Services'],
    ), name='ndt_service'),

    path('dharla-logistics/', TemplatePageView.as_view(
        template_name = "pages/dharla_logistics.html",
        image_urls = ['assets/img/slider/Dharla-banner-01.jpg', 
                      'assets/img/slider/Dharla-banner-01.jpg', 
                      'assets/img/slider/slide17.jpg'],
        banner_texts = ['Dharla Logistics', 
                        'Dharla Logistics', 
                        'Dharla Logistics'],
    ), name='dharla_logistics'),
    
    path('maintenance/', TemplatePageView.as_view(
        template_name = "pages/maintenance.html",
    ), name='maintenance'),
    # All Project List
    path('project/on-going/new-building', NewBuildingProjectListView.as_view(), name='new_building_project_list'),
    path('project/on-going/repair', RepairProjectListView.as_view(), name='repair_project_list'),
    path('project/completed', CompletedProjectListView.as_view(), name='completed_project_list'),
    path('project/details/<int:pk>', ProjectDetailView.as_view(), name='project_details'),
    # news and insight urls
    path('news-insight/list', NewsInsightListView.as_view(), name='news_insight_list'),
    path('news-insight/details/<int:pk>', NewsDetailView.as_view(), name='news_insight_details'),
    # Carrier and Job Post List
    path('job-post/list', JobPostListView.as_view(), name='job_post_list'),
    path('job-post/details/<int:pk>', NewsDetailView.as_view(
        model = JobPost,
        template_name = 'pages/job_details.html'
    ), name='job_post_details'),
    # CONTACT US URL 
    path('contact-us/form', ContactUsCreateView.as_view(), name='contact_us_create'),
    # DOCKING CERTIFICATE
    path('docking-certificate/search', DockingCertificateSearchView.as_view(), name='docking_certificate_search'),
    path('docking-certificate/details/<str:certificate_no>/', DockingCertificateDetailView.as_view(), name='docking_certificate_details'),
    # TEAM MEMBERS URLS.
    path('team-members/list', TeamMemberListView.as_view(), name='team_members_list'),
    path('team-member/details/<int:pk>', NewsDetailView.as_view(
        model = TeamMember,
        template_name = 'pages/team_details.html'
    ), name='team_member_details'),

]