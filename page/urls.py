from django.urls import path
from .views import TemplatePageView


urlpatterns = [
    path('shipbuilding/', TemplatePageView.as_view(
        template_name = "pages/service_details.html",
        image_urls = ['assets/img/slider/slide19.jpg', 'assets/img/slider/slide16.jpg', 'assets/img/slider/slide17.jpg']
    ), name='shipbuilding'),
]