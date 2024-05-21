from django.urls import path, include 
from ta_device.calendar.views import (HolidayCreateView, HolidayListView, HolidayUpdateView, 
                                    HolidayCalendarCreateView, HolidayCalendarListView, HolidayCalendarUpdateView)


urlpatterns = [
    path('create/', HolidayCalendarCreateView.as_view(), name='calendar_create'),
    path('update/<int:pk>', HolidayCalendarUpdateView.as_view(), name='calendar_update'),
    path('all-list/', HolidayCalendarListView.as_view(), name='all_calendar_list'),
    # HOLIDAY
    path('holiday/create/', HolidayCreateView.as_view(), name='holiday_create'),
    path('holiday/update/<int:pk>', HolidayUpdateView.as_view(), name='holiday_update'),
    path('holiday/all-list/', HolidayListView.as_view(), name='all_holiday_list'),
]