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
        "test",
        "begin",
        "result",
    )
    search_fields = (
        "user",
        "test",
    )
    readonly_fields = (
        "user",
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
        "information",
        "test",
        "begin",
        "result",
    )
    search_fields = (
        "information",
        "test",
    )
    readonly_fields = (
        "information",
        "test",
        "begin",
        "end",
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
