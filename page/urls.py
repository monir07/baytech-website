from django.urls import path
from .views import (TemplatePageView, NewBuildingProjectListView, 
                    ProjectDetailView, CompletedProjectListView, RepairProjectListView, 
                    NewsInsightListView, NewsDetailView, JobPostListView, ContactUsCreateView)
from .models import (JobPost)


urlpatterns = [
    path('shipbuilding/', TemplatePageView.as_view(
        template_name = "pages/service_details.html",
        image_urls = ['assets/img/slider/slide19.jpg', 'assets/img/slider/slide16.jpg', 'assets/img/slider/slide17.jpg']
    ), name='shipbuilding'),

    path('project/on-going/new-building', NewBuildingProjectListView.as_view(), name='new_building_project_list'),
    path('project/on-going/repair', RepairProjectListView.as_view(), name='repair_project_list'),
    path('project/completed', CompletedProjectListView.as_view(), name='completed_project_list'),
    path('project/details/<int:pk>', ProjectDetailView.as_view(), name='project_details'),
    # news and insight urls
    path('news-insight/list', NewsInsightListView.as_view(), name='news_insight_list'),
    path('news-insight/details/<int:pk>', NewsDetailView.as_view(), name='news_insight_details'),
    # Job Post List
    path('job-post/list', JobPostListView.as_view(), name='job_post_list'),
    path('job-post/details/<int:pk>', NewsDetailView.as_view(
        model = JobPost,
        template_name = 'pages/job_details.html'
    ), name='job_post_details'),
    # CONTACT US URL 
    path('contact-us/form', ContactUsCreateView.as_view(), name='contact_us_create')

]