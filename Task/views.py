from django.views.generic import CreateView, UpdateView
from .forms import MultiplyChoiceTestWithAnswersForm
from .models import *
from typing import Any, Dict


class MultiplyChoiceTestCreateView(CreateView):
    form_class = MultiplyChoiceTestWithAnswersForm
    template_name = "multiply_choice_test_create.html"

    def get_success_url(self):
        return "create"


class MultiplyChoiceTestUpdateView(UpdateView):
    form_class = MultiplyChoiceTestWithAnswersForm
    model = MultiplyChoiceTest
    template_name = "multiply_choice_test_update.html"

    def get_success_url(self):
        return f"update={self.kwargs['pk']}"
