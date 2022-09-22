from cgitb import lookup
import email
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import SetPasswordForm, PasswordResetForm
from django.urls import exceptions as url_exceptions
from django.utils.encoding import force_str
from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from allauth.account.adapter import get_adapter
from dj_rest_auth.registration.serializers import RegisterSerializer

from allauth.account.models import EmailAddress, EmailConfirmation

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    User model w/o password
    """

    @staticmethod
    def validate_username(username):
        if "allauth.account" not in settings.INSTALLED_APPS:
            # We don't need to call the all-auth
            # username validator unless its installed
            return username

        # from allauth.account.adapter import get_adapter

        username = get_adapter().clean_username(username)
        return username

    class Meta:
        extra_fields = []
        # see https://github.com/iMerica/dj-rest-auth/issues/181
        # UserModel.XYZ causing attribute error while importing other
        # classes from `serializers.py`. So, we need to check whether the auth model has
        # the attribute or not
        if hasattr(UserModel, "USERNAME_FIELD"):
            extra_fields.append(UserModel.USERNAME_FIELD)
        if hasattr(UserModel, "EMAIL_FIELD"):
            extra_fields.append(UserModel.EMAIL_FIELD)
        if hasattr(UserModel, "first_name"):
            extra_fields.append("first_name")
        if hasattr(UserModel, "last_name"):
            extra_fields.append("last_name")
        if hasattr(UserModel, "phone"):
            extra_fields.append("phone")
        if hasattr(UserModel, "address"):
            extra_fields.append("address")
        if hasattr(UserModel, "gender"):
            extra_fields.append("gender")
        if hasattr(UserModel, "is_customer"):
            extra_fields.append("is_customer")
        if hasattr(UserModel, "is_tailor"):
            extra_fields.append("is_tailor")
        if hasattr(UserModel, "date_joined"):
            extra_fields.append("date_joined")
        model = UserModel
        fields = ("pk", *extra_fields)
        read_only_fields = ("email",)


class CustomRegisterSerializer(RegisterSerializer):
    """
    Custom register serializer to add extra fields
    """

    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    phone = serializers.CharField(required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)
    gender = serializers.ChoiceField(
        choices=("Male", "Male", "Female", "Female"), required=False, allow_blank=True
    )
    is_customer = serializers.BooleanField(required=False, default=False)
    is_tailor = serializers.BooleanField(required=False, default=False)

    def save(self, request):
        user = super().save(request)
        user.first_name = self.data.get("first_name")
        user.last_name = self.data.get("last_name")
        user.phone = self.data.get("phone")
        user.address = self.data.get("address")
        user.gender = self.data.get("gender")
        user.is_customer = self.data.get("is_customer")
        user.is_tailor = self.data.get("is_tailor")
        user.save()
        return user


# create a serializer for the email model
class EmailAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailAddress
        fields = ["user", "email", "verified", "primary"]
        depth = 1


class CombineEmailUser(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = EmailAddress
        fields = ("user", "email", "verified", "primary")


class EmailConfirmationUser(serializers.ModelSerializer):
    # emails = EmailAddressSerializer(read_only=True)

    class Meta:
        model = EmailConfirmation
        fields = ("email_address", "key", "sent", "created")
