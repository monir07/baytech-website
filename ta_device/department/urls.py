from django.urls import path, include 
from ta_device.employee.views import (EmployeeCreateView, EmployeeListView, EmployeeUpdateView)


urlpatterns = [
    path('create/', EmployeeCreateView.as_view(), name='employee_create'),
    path('update/<int:pk>', EmployeeUpdateView.as_view(), name='employee_update'),
    path('all-list/', EmployeeListView.as_view(), name='all_employee_list'),
]