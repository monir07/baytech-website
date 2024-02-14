from django.http import HttpResponseRedirect
from django.utils import timezone
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin


def get_time_difference(user):
    max_password_age = settings.MAX_PASSWORD_AGE
    if not user.last_password_changed:
        return False
    pass_age_difference = (timezone.now() - user.last_password_changed).total_seconds()
    return pass_age_difference > max_password_age and user.password_expires


class ForcePasswordChangeMiddleware(MiddlewareMixin):
    """Checking User needs to force redirect to change password view or not"""

    def process_request(self, request):
        # if not request.user.is_authenticated:
        #     return HttpResponseRedirect(settings.LOGIN_URL)
        
        if request.path in settings.ACCESSIBLE_URLS:
            return self.get_response(request)
        
        max_pass_age_expired = get_time_difference(request.user)
        if request.user.change_password_required or max_pass_age_expired:
            if request.path not in settings.ACCESSIBLE_URLS:
                return HttpResponseRedirect(settings.PASSWORD_CHANGE_URL)
        return