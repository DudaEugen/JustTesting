from django.contrib import admin
from .models import *
from .forms import M2MTaskListInTestForm


class TaskListInTestInline(admin.TabularInline):
    model = Test.task_lists.through
    form = M2MTaskListInTestForm
    extra = 0
    verbose_name = "Список питань"
    verbose_name_plural = "Списки питань"


class TestAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "is_allowed",
        "is_allow_for_unautorized_users",
    )
    search_fields = (
        "name",
    )
    list_filter = (
        "is_allowed",
        "is_allow_for_unautorized_users",
    )
    inlines = (
        TaskListInTestInline,
    )


admin.site.register(Test, TestAdmin)
