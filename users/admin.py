from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import NewUser

# Register your models here.

fields = list(UserAdmin.fieldsets)
fields[1] = (
    "Personal info",
    {
        "fields": (
            "first_name",
            "last_name",
            "email",
            "phone",
            "address",
            "gender",
            "is_customer",
            "is_tailor",
        )
    },
)
UserAdmin.fieldsets = tuple(fields)

admin.site.register(NewUser, UserAdmin)
