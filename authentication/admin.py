from django.contrib import admin

# Register your models here.

from authentication.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # date_hierarchy = 'created_at'
    list_display = (
        "username",
        "email",
        "phone_number",
        "usergroup",
        "name",
    )
    search_fields = [
        "username",
        "usergroup",
        "name",
        "email",
        "phone_number",
    ]
    readonly_fields = ["username"]
