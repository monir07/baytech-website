from django.urls import path, include 
from ta_device.device.views import (DeviceCreateView, DeviceListView, DeviceUpdateView)


urlpatterns = [
    path('create/', DeviceCreateView.as_view(), name='device_create'),
    path('update/<int:pk>', DeviceUpdateView.as_view(), name='device_update'),
    path('all-list/', DeviceListView.as_view(), name='device_all_list'),
]