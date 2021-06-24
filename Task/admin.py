from django.contrib import admin
from .models import *


class AnswerForMultiplyCMultiplyChoiceTestAnswerInline(admin.TabularInline):
    model = MultiplyChoiceTestAnswer
    extra = 0
    verbose_name = "Варіант відповіді"
    verbose_name_plural = "Варіанти відповіді"


class TaskListAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
    )
    search_fields = (
        "name",
    )


class MultiplyChoiceTestAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "__str__",
        "task_list",
    )
    search_fields = (
        "text",
    )
    inlines = (
        AnswerForMultiplyCMultiplyChoiceTestAnswerInline,
    )


admin.site.register(TaskList, TaskListAdmin)
admin.site.register(MultiplyChoiceTest, MultiplyChoiceTestAdmin)
