from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from djangoql.admin import DjangoQLSearchMixin

# from .models import SomeModel
from .models import User

admin.site.register(User, UserAdmin)


# @admin.register(SomeModel)
# class SomeModelAdmin(DjangoQLSearchMixin, admin.ModelAdmin):
#     list_display = ["user", "timestamp", "message"]
#     list_filter = ("timestamp",)
