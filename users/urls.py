from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls


from . import views


urlpatterns = [
    path("emails", views.user, name="email-list"),
    # re_path(r"^emails/?<email>/$", views.one_user, name="email-list-search"),
    path("activations/", views.activation, name="activation-list"),
]
