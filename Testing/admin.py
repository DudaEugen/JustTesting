from django.contrib import admin
from .models import TestingSessionOfAutorizedUser, TestingSessionOfUnautorizedUser


class TaskInTestingSessionInline(admin.TabularInline):
    from .models import TestingSession

    model = TestingSession.tasks.through
    readonly_fields = (
        "task",
        "is_completed",
        "order",
    )
    can_delete = False
    extra = 0
    verbose_name = "Завдання"
    verbose_name_plural = "Завдання"


class TestingSessionOfAutorizedUserAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "group",
        "test",
        "begin",
        "result",
    )
    search_fields = (
        "user",
        "group",
        "test",
    )
    readonly_fields = (
        "user",
        "group",
        "test",
        "begin",
        "end",
        "result",
    )
    inlines = (
        TaskInTestingSessionInline,
    )


class TestingSessionOfUnautorizedUserAdmin(admin.ModelAdmin):
    list_display = (
        "display_name",
        "group",
        "test",
        "begin",
        "ip_begin",
        "result",
    )
    search_fields = (
        "display_name",
        "group",
        "test",
        "ip_begin",
    )
    readonly_fields = (
        "display_name",
        "group",
        "test",
        "begin",
        "end",
        "ip_begin",
        "result",
    )
    inlines = (
        TaskInTestingSessionInline,
    )


admin.site.register(
    TestingSessionOfAutorizedUser,
    TestingSessionOfAutorizedUserAdmin
)
admin.site.register(
    TestingSessionOfUnautorizedUser,
    TestingSessionOfUnautorizedUserAdmin
)
