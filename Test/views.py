from django.views.generic import CreateView, UpdateView
from .forms import TestWithTaskListForm
from .models import *
from django.utils.decorators import method_decorator
from JustTesting.utils.permission_decorators import user_permissions_decorator
from typing import Dict, Any


@method_decorator(user_permissions_decorator, name="dispatch")
class TestCreateView(CreateView):
    form_class = TestWithTaskListForm
    template_name = "Test/test_create.html"

    def get_success_url(self):
        return "create"


@method_decorator(user_permissions_decorator, name="dispatch")
class TestUpdateView(UpdateView):
    form_class = TestWithTaskListForm
    model = Test
    template_name = "Test/test_update.html"

    def get_success_url(self):
        return f"update={self.kwargs['pk']}"
