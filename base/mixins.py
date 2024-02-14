from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import UpdateView
from django.db import transaction
from django.shortcuts import HttpResponseRedirect


class CustomPermissionMixin(PermissionRequiredMixin):
    permission_required = ""
    allowed_roles=[]
    def has_permission(self) -> bool:
        perms = self.get_permission_required()
        has_permss = self.request.user.has_perms(perms)
        if self.request.user.groups.exists():
            groups = self.request.user.groups.all()
            for group in groups:
                if group.name in self.allowed_roles:
                    return True
            return has_permss
        return has_permss

class UnauthenticatedUserMixin(PermissionRequiredMixin):
    def has_permission(self) -> bool:
        return not self.request.user.is_authenticated()


class CommonMixin(SuccessMessageMixin, LoginRequiredMixin, CustomPermissionMixin):
    permission_required = ""
    permission_denied_message = 'You don not have permission'
    title = ""
    url = ""

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)
        data['title'] = self.title
        data['url'] = self.url
        return data
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # kwargs.update({
        #     'request': self.request,
        #     'view': self
        # })
        return kwargs

class AuthUserMixin(SuccessMessageMixin, LoginRequiredMixin):
    title = ""
    success_url = ""
    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)
        data['title'] = self.title
        return data

    def get_success_url(self) -> str:
        return self.success_url


class BaseUpdateView(UpdateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update_url'] = self.request.resolver_match.url_name
        return context
    
    def form_valid(self, form, *args, **kwargs):
        self.object = form.save(commit=False)
        self.object.updated_by = self.request.user
        with transaction.atomic():
            self.object.save()
        return HttpResponseRedirect(self.get_success_url())