from django.urls import path, include
from django.urls.conf import re_path
from core.views import health_check, HomePageView, reference_page
from core.settings import DEBUG
from django.contrib import admin
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from user import urls as user_urls
from user import urls_api as user_api
from django.conf import settings
from django.conf.urls.static import static
from page import urls as page_urls


schema_view = get_schema_view(
    openapi.Info(
        title="Project API Documentation",
        default_version='v1.0',
        description="Api description",
        contact=openapi.Contact(email="mdfahadhossain71@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=False,
    permission_classes=(permissions.IsAuthenticated,),
)

v1_patterns = [
    path('', health_check),
    path('users/', include(user_api)),
]

    
urlpatterns = [
    re_path(r'^.*\.html', reference_page, name='ref_page'),
    path('', HomePageView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('users/', include(user_urls)),
    path('api/', include([
        path('v1.0/', include(v1_patterns))
    ])),

    # page urls
    path('', include(page_urls)),
]

urlpatterns += [path('api-auth/', include('rest_framework.urls')),]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if DEBUG:
    urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]
    urlpatterns += [
        re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ]

admin.site.site_header = "TAM Admin"
admin.site.site_title = "TAM Admin Portal"
admin.site.index_title = "Welcome to TAM"

handler400 = 'base.views.custom_error_400'
handler403 = 'base.views.custom_error_403'
handler404 = 'base.views.custom_error_404'
handler405 = 'base.views.custom_error_405'