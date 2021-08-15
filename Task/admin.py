from django.contrib import admin
from .models import *
from .forms import MultipleChoiceTestAnswerInlineFormset
from Test.models import Test


class MultipleChoiceTestAnswerInline(admin.TabularInline):
    model = MultipleChoiceTestAnswer
    formset = MultipleChoiceTestAnswerInlineFormset
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


class TaskListInKnowledgeFieldInline(admin.TabularInline):
    model = TaskList
    extra = 0
    verbose_name = "Список завдань"
    verbose_name_plural = "Списки завдань"


class KnowledgeFieldAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
    )
    search_fields = (
        "name",
    )
    inlines = (
        TaskListInKnowledgeFieldInline,
    )


class TaskListAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
    )
    search_fields = (
        "name",
        "knowledge_field__name",
    )
    inlines = (
        TestInTaskListInline,
    )


class MultipleChoiceTestAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "__str__",
        "task_list",
    )
    search_fields = (
        "text",
    )
    inlines = (
        MultipleChoiceTestAnswerInline,
    )


admin.site.register(KnowledgeField, KnowledgeFieldAdmin)
admin.site.register(TaskList, TaskListAdmin)
admin.site.register(MultipleChoiceTest, MultipleChoiceTestAdmin)
