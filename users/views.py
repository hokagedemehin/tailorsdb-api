from re import search
from allauth.account.models import EmailAddress, EmailConfirmation
from rest_framework.mixins import ListModelMixin
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework import viewsets
from .serializers import (
    CombineEmailUser,
    EmailConfirmationUser,
    EmailAddressSerializer,
)

# from .serializers import EmailAddressSerializer


# create a class list view that will list all the email address in the database


# class EmailAddressListView(ListModelMixin, GenericAPIView):
class EmailAddressListView(viewsets.ReadOnlyModelViewSet):
    queryset = EmailAddress.objects.all()
    serializer_class = CombineEmailUser
    # lookup_field = "pk"
    filterset_fields = ["email"]
    # search_fields = ["email"]
    # serializer_class = EmailAddressSerializer

    # def get(self, request, *args, **kwargs):
    #     return self.list(request, *args, **kwargs)


# user = EmailAddressListView.as_view()


class OneEmailAddressListView(ListModelMixin, GenericAPIView):
    queryset = EmailAddress.objects.all()
    serializer_class = EmailAddressSerializer
    # lookup_url_kwarg = "email"
    # serializer_class = EmailAddressSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


one_user = OneEmailAddressListView.as_view()


class EmailConfirmationUserView(ListModelMixin, GenericAPIView):
    queryset = EmailConfirmation.objects.all()
    serializer_class = EmailConfirmationUser

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


activation = EmailConfirmationUserView.as_view()
