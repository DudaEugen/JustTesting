from django.views.generic import CreateView, UpdateView
from .forms import MultipleChoiceTestWithAnswersForm
from .models import *
from JustTesting.utils.template_filters import to_int


class MultipleChoiceTestCreateView(CreateView):
    form_class = MultipleChoiceTestWithAnswersForm
    template_name = "multiple_choice_test_create.html"

    def get_success_url(self):
        return "create"


class MultipleChoiceTestUpdateView(UpdateView):
    form_class = MultipleChoiceTestWithAnswersForm
    model = MultipleChoiceTest
    template_name = "multiple_choice_test_update.html"

    def get_success_url(self):
        return f"update={self.kwargs['pk']}"
