from django.contrib import admin
from .models import TestSessionOfAutorizedUser, TestSessionOfUnautorizedUser


class TaskInTestSessionInline(admin.TabularInline):
    from .models import TestSession

    model = TestSession.tasks.through
    readonly_fields = (
        "task",
        "is_completed",
        "order",
    )
    can_delete = False
    extra = 0
    verbose_name = "Завдання"
    verbose_name_plural = "Завдання"


class TestSessionOfAutorizedUserAdmin(admin.ModelAdmin):
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
        TaskInTestSessionInline,
    )


class TestSessionOfUnautorizedUserAdmin(admin.ModelAdmin):
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
        TaskInTestSessionInline,
    )


admin.site.register(
    TestSessionOfAutorizedUser,
    TestSessionOfAutorizedUserAdmin
)
admin.site.register(
    TestSessionOfUnautorizedUser,
    TestSessionOfUnautorizedUserAdmin
)
