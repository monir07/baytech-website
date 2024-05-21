from django.urls import path, include 
from ta_device.department.views import (SectionCreateView, SectionListView, SectionUpdateView, 
                                    DepartmentCreateView, DepartmentListView, DepartmentUpdateView)


urlpatterns = [
    path('section/create/', SectionCreateView.as_view(), name='section_create'),
    path('section/update/<int:pk>', SectionUpdateView.as_view(), name='section_update'),
    path('section/all-list/', SectionListView.as_view(), name='all_section_list'),
    # Department
    path('create/', DepartmentCreateView.as_view(), name='department_create'),
    path('update/<int:pk>', DepartmentUpdateView.as_view(), name='department_update'),
    path('all-list/', DepartmentListView.as_view(), name='all_department_list'),
]