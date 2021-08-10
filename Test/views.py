from django.views.generic import CreateView, UpdateView
from .forms import TestWithTaskListForm
from .models import *


class TestCreateView(CreateView):
    form_class = TestWithTaskListForm
    template_name = "Test/test_create.html"

    def get_success_url(self):
        return "create"


class TestUpdateView(UpdateView):
    form_class = TestWithTaskListForm
    model = Test
    template_name = "Test/test_update.html"

    def get_success_url(self):
        return f"update={self.kwargs['pk']}"
