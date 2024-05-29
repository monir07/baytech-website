from django.urls import path, include 
from ta_device.employee.views import (EmployeeCreateView, EmployeeListView, EmployeeUpdateView, EmployeeDeleteView)


urlpatterns = [
    path('create/', EmployeeCreateView.as_view(), name='employee_create'),
    path('update/<int:pk>', EmployeeUpdateView.as_view(), name='employee_update'),
    path('delete/<int:pk>', EmployeeDeleteView.as_view(), name='employee_delete'),
    path('all-list/', EmployeeListView.as_view(), name='all_employee_list'),
]