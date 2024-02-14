from django.shortcuts import render, redirect
from django.http.response import HttpResponseRedirect
from django.db import transaction
from django.views import View
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.contrib.auth.views import (LoginView, LogoutView)
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.mixins import LoginRequiredMixin

# Email Validation Works related Imports
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from base.mixins import UnauthenticatedUserMixin
from user.forms import RegisterForm
User = get_user_model()


class UserSignUpView(View, UnauthenticatedUserMixin):
    success_url = reverse_lazy("home")
    template_name = "base/common/form.html"

    def get_context_data(self, **kwargs):
        if "form" not in kwargs:
            form = RegisterForm()
        else:
            form = kwargs.get('form')
        return {
            "form": form,
        }

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            with transaction.atomic():
                user = form.save(commit=False)
                user.is_active = True
                user.save()
                login(self.request, user)
                current_site = get_current_site(request)
                mail_subject = 'Activate your account.'
                message = render_to_string('user/acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
                messages.info(request, 'Please confirm From your email address to complete the registration and Then you can login')
        else:
            messages.error(request, form.errors)
            context = self.get_context_data(signup_form=form)
            return render(request, self.template_name, context)
        return HttpResponseRedirect(self.success_url)

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.info(request, f"Thank you for your email confirmation.  Now you can login your account. {user}")
        return redirect('login')
    else:
        messages.warning(request, 'Activation link is invalid!')
        return redirect('signup')


class UserLoginView(LoginView, UnauthenticatedUserMixin):
    form_class = AuthenticationForm
    template_name = 'user/login.html'
    success_message = 'Login successfully'

    def form_valid(self, form):
        login(self.request, form.get_user())
        next_link = self.request.GET.get('next')
        if next_link:
            return redirect(next_link)
        else:
            return HttpResponseRedirect(reverse_lazy('home'))
    
    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)


class UserLogoutView(LogoutView, LoginRequiredMixin):
    next_page = reverse_lazy("login")