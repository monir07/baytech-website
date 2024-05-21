from django.urls import path, include 
from ta_device.attendance.views import (AttendanceCreateView, AttendanceListView, AttendanceUpdateView)


urlpatterns = [
    path('create/', AttendanceCreateView.as_view(), name='attendance_create'),
    path('update/<int:pk>', AttendanceUpdateView.as_view(), name='attendance_update'),
    path('all-list/', AttendanceListView.as_view(), name='all_attendance_list'),
]