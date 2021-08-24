from django.views.generic import CreateView, UpdateView, ListView
from .forms import MultipleChoiceTestWithAnswersForm
from .models import *
from django.utils.decorators import method_decorator
from JustTesting.utils.permission_decorators import user_permissions_decorator


@method_decorator(user_permissions_decorator, name="dispatch")
class TaskListView(ListView):
    model = TaskList
    template_name = "Task/task_lists.html"
    context_object_name = "task_lists"


@method_decorator(user_permissions_decorator, name="dispatch")
class MultipleChoiceTestsOfTaskLisk(ListView):
    template_name = "Task/multiple_choice_test_of_task_list.html"
    context_object_name = "task_list"

    def get_queryset(self):
        return MultipleChoiceTest.objects.filter(task_list_id=self.kwargs["task_list_pk"])


@method_decorator(user_permissions_decorator, name="dispatch")
class MultipleChoiceTestCreateView(CreateView):
    form_class = MultipleChoiceTestWithAnswersForm
    template_name = "Task/multiple_choice_test_create.html"

    def get_success_url(self):
        return "create"


@method_decorator(user_permissions_decorator, name="dispatch")
class MultipleChoiceTestUpdateView(UpdateView):
    form_class = MultipleChoiceTestWithAnswersForm
    model = MultipleChoiceTest
    template_name = "Task/multiple_choice_test_update.html"

    def get_success_url(self):
        return f"update={self.kwargs['pk']}"
