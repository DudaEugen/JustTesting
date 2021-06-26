from django.views.generic import CreateView
from .forms import MultiplyChoiceTestWithAnswersForm
from .models import *
from typing import Any, Dict


class MultiplyChoiceTestCreateView(CreateView):
    form_class = MultiplyChoiceTestWithAnswersForm
    template_name = "multiply_choice_test_create.html"

    def get_success_url(self):
        return "create"
