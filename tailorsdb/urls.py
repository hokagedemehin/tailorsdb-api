"""tailorsdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls
from rest_framework import routers

# from dj_rest_auth.views import (
#     # LoginView,
#     # LogoutView,
#     # PasswordChangeView,
#     PasswordResetConfirmView,
#     # PasswordResetView,
#     # UserDetailsView,
# )
from django.views.generic import TemplateView, RedirectView

from . import views
from users import views as user_views
from users.views import EmailAddressListView

router = routers.SimpleRouter()
router.register(r"users", EmailAddressListView)

urlpatterns = [
    # re_path(r"^$", TemplateView.as_view(template_name="home.html"), name="home"),
    path("accounts/login/", views.login, name="account_login"),
    path("accounts/email/", views.email, name="account_email"),
    re_path(
        r"^password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,32})/$",
        TemplateView.as_view(template_name="password_reset_confirm.html"),
        name="password_reset_confirm",
    ),
    re_path(
        r"^email-verification/$",
        TemplateView.as_view(template_name="email_verification.html"),
        name="email-verification",
    ),
    re_path(
        r"^password-reset/$",
        TemplateView.as_view(template_name="password_reset.html"),
        name="password-reset",
    ),
    re_path(
        r"^password-reset/confirm/$",
        TemplateView.as_view(template_name="password_reset_confirm.html"),
        name="password-reset-confirm",
    ),
    re_path(
        r"^password-change/$",
        TemplateView.as_view(template_name="password_change.html"),
        name="password-change",
    ),
    # re_path(
    #     r"^password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,32})/$",
    #     TemplateView.as_view(template_name="password_reset_confirm.html"),
    #     name="password_reset_confirm",
    # ),
    # re_path(
    #     r"^password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,32})/$",
    #     TemplateView.as_view(template_name="password_reset_from_key.html"),
    #     name="password_reset_confirm",
    # ),
    # re_path(
    #     r"^password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,32})/$",
    #     PasswordResetConfirmView.as_view(),
    #     name="password_reset_confirm",
    # ),
    re_path(
        r"^resend-email-verification/$",
        TemplateView.as_view(template_name="resend_email_verification.html"),
        name="resend-email-verification",
    ),
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("dj-rest-auth/", include("dj_rest_auth.urls")),
    path("docs/", include_docs_urls("TailorsAPI")),
    path("dj-rest-auth/registration/", include("dj_rest_auth.registration.urls")),
    path(
        "schema/",
        get_schema_view(
            title="TailorsDB",
            description="API to get and save client's measurement data",
            version="1.0.0",
        ),
        name="openapi-schema",
    ),
    path("accounts/", include("allauth.urls")),
    re_path(
        r"^accounts/profile/$",
        RedirectView.as_view(url="/", permanent=True),
        name="profile-redirect",
    ),
    path("", include(router.urls)),
    path("__reload__/", include("django_browser_reload.urls")),
]
