from django.views.generic import CreateView, UpdateView
from .forms import MultipleChoiceTestWithAnswersForm
from .models import *
from django.utils.decorators import method_decorator
from JustTesting.utils.permission_decorators import user_permissions_decorator


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
