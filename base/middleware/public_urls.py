from django.http.request import split_domain_port
from django.utils.deprecation import MiddlewareMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.conf import settings


class ProcessPublicRequestMiddleware(MiddlewareMixin):
    """
    This middleware appends new payload in request body
    """

    def process_request(self, request):
        host = request.get_host()
        domain, port = split_domain_port(host)

        redirect_url = "/"
        if request.path == redirect_url:
            return self.get_response(request)
        
        if not request.user.is_authenticated:
            return HttpResponseRedirect(settings.LOGIN_URL)
    
        if domain not in settings.ACCEPTABLE_DOMAINS:
            if request.path in settings.ACCESSIBLE_URLS:
                pass
            elif request.path.split("/")[1] not in settings.PUBLIC_URL_STARTS_WITH:
                raise PermissionDenied
        return