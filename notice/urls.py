from django.urls import path
from notice.views import (NoticePublishListView, NoticeDetailView, 
                          NocPublishListView, NocDetailView)

urlpatterns = [
    path('publish-list/', NoticePublishListView.as_view(), name='notice_publish_list'),
    path('details/<int:pk>', NoticeDetailView.as_view(), name='notice_details'),

    path('noc/publish-list/', NocPublishListView.as_view(), name='noc_publish_list'),
    path('noc/details/<int:pk>', NocDetailView.as_view(), name='noc_details'),
    
]