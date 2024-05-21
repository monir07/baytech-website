from django.urls import path, include 
from ta_device.shift.views import (ShiftCreateView, ShiftListView, ShiftUpdateView)


urlpatterns = [
    path('create/', ShiftCreateView.as_view(), name='shift_create'),
    path('update/<int:pk>', ShiftUpdateView.as_view(), name='shift_update'),
    path('all-list/', ShiftListView.as_view(), name='all_shift_list'),
]