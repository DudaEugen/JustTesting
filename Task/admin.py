from django.contrib import admin
from .models import *
from .forms import MultiplyChoiceTestAnswerInlineFormset


class MultiplyChoiceTestAnswerInline(admin.TabularInline):
    model = MultiplyChoiceTestAnswer
    formset = MultiplyChoiceTestAnswerInlineFormset
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
        MultiplyChoiceTestAnswerInline,
    )


admin.site.register(TaskList, TaskListAdmin)
admin.site.register(MultiplyChoiceTest, MultiplyChoiceTestAdmin)
