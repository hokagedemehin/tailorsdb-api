from allauth.account.views import LoginView, EmailView

from allauth.account.utils import (
    passthrough_next_redirect_url,
)
from allauth.account.models import EmailAddress
from dj_rest_auth.views import (
    PasswordResetView,
)
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.response import Response

# from .serializers import CustomPasswordReset
from django.urls import reverse, reverse_lazy
from allauth.utils import get_request_param
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.sites.models import Site

from django.contrib.auth.decorators import login_required

import environ
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))


class CustomLoginView(LoginView):
    # template_name = "login1.html"

    def get_context_data(self, **kwargs):
        ret = super(LoginView, self).get_context_data(**kwargs)
        signup_url = passthrough_next_redirect_url(
            self.request, reverse("account_signup"), self.redirect_field_name
        )
        redirect_field_value = get_request_param(self.request, self.redirect_field_name)
        site = get_current_site(self.request)
        # site1 = Site.objects.get_current()

        # print("site", site)
        # print("site1", site1)
        profile_url1 = env("FRONTEND_PROFILE_URL")
        # if "localhost" in site.domain:
        #     profile_url1 = env("FRONTEND_PROFILE_URL")
        # else:
        #     profile_url1 = "https://new.tailorsdb.com/profile"
        ret.update(
            {
                "signup_url": signup_url,
                "site": site,
                "redirect_field_name": self.redirect_field_name,
                "redirect_field_value": redirect_field_value,
                "profile_url1": profile_url1,
            }
        )
        return ret


login = CustomLoginView.as_view()


class CustomEmailView(EmailView):
    def get_context_data(self, **kwargs):
        ret = super(EmailView, self).get_context_data(**kwargs)
        ret["add_email_form"] = ret.get("form")
        ret["can_add_email"] = EmailAddress.objects.can_add_email(self.request.user)

        profile_url1 = env("FRONTEND_PROFILE_URL")
        ret["profile_url1"] = profile_url1
        return ret


email = login_required(CustomEmailView.as_view())


# class CustomPasswordResetView(PasswordResetView):
#     serializer_class = CustomPasswordReset

#     def post(self, request, *args, **kwargs):
#         # Create a serializer with request.data
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         serializer.save()
#         # Return the success message with OK HTTP status
#         return Response(
#             {"detail": _("Password reset e-mail has been sent.")},
#             status=status.HTTP_200_OK,
#         )
