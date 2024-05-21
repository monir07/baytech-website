from django.urls import path, include 
from ta_device.attendance import urls as attendance_urls
from ta_device.calendar import urls as calendar_urls
from ta_device.device import urls as device_urls
from ta_device.employee import urls as employee_urls


urlpatterns = [
    # path('', HomePageView.as_view(), name='home'),
    path('attendance/', include(attendance_urls)),
    path('calender/', include(calendar_urls)),
    path('device/', include(device_urls)),
    path('employee/', include(employee_urls)),
]