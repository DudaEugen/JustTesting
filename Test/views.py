from django.views.generic import CreateView, UpdateView
from .forms import TestWithTaskListForm
from .models import *
from JustTesting.utils.template_filters import to_int


class TestCreateView(CreateView):
    form_class = TestWithTaskListForm
    template_name = "test_create.html"

    def get_success_url(self):
        return "create"


class TestUpdateView(UpdateView):
    form_class = TestWithTaskListForm
    model = Test
    template_name = "test_update.html"

    def get_success_url(self):
        return f"update={self.kwargs['pk']}"
