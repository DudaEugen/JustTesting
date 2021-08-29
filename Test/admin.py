from django.contrib import admin
from .models import *


class TaskListInTestInline(admin.TabularInline):
    model = Test.task_lists.through
    extra = 0
    verbose_name = "Список питань"
    verbose_name_plural = "Списки питань"


class TestAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "is_allowed",
        "is_allow_for_unautorized_users",
        "is_allow_help",
        "show_right_solution_after_mistake",
        "repeat_unresolved_tasks",
        "is_allow_skip_task",
    )
    search_fields = (
        "name",
    )
    list_filter = (
        "is_allowed",
        "is_allow_for_unautorized_users",
        "is_allow_help",
        "show_right_solution_after_mistake",
        "repeat_unresolved_tasks",
        "is_allow_skip_task",
    )
    inlines = (
        TaskListInTestInline,
    )


admin.site.register(Test, TestAdmin)
