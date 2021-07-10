from django.contrib import admin
from .models import *
from .forms import MultiplyChoiceTestAnswerInlineFormset
from Test.models import Test


class MultiplyChoiceTestAnswerInline(admin.TabularInline):
    model = MultiplyChoiceTestAnswer
    formset = MultiplyChoiceTestAnswerInlineFormset
    extra = 0
    verbose_name = "Варіант відповіді"
    verbose_name_plural = "Варіанти відповіді"


class TestInTaskListInline(admin.TabularInline):
    model = Test.task_lists.through
    extra = 0
    verbose_name = "Список питань"
    verbose_name_plural = "Списки питань"
    readonly_fields = ("test", "task_count")
    can_delete = False


class TaskListAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
    )
    search_fields = (
        "name",
    )
    inlines = (
        TestInTaskListInline,
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
