from django.http.response import HttpResponseRedirect
from django.views.generic import CreateView, FormView
from django.shortcuts import get_object_or_404
from .models import *
from .forms import TestingSessionOfAutorizedUserForm, TestingSessionOfUnautorizedUserForm


class TestingSessionCreateView(CreateView):
    template_name = "test_session_create.html"
    success_url = "start"

    def get_form(self, form_class=None):
        if self.request.user.is_authenticated:
            if self.request.POST:
                return TestingSessionOfAutorizedUserForm(self.request.POST)
            return TestingSessionOfAutorizedUserForm()
        else:
            if self.request.POST:
                return TestingSessionOfUnautorizedUserForm(self.request.POST)
            return TestingSessionOfUnautorizedUserForm()

    def form_valid(self, form) -> HttpResponseRedirect:
        test_session = form.save(commit=False)
        if self.request.user.is_authenticated:
            test_session.user = self.request.user
            test_session.save()
        else:
            test_session.save(self.request.session)
        self.kwargs["session"] = test_session
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self) -> str:
        return f"session={self.kwargs['session'].pk}"


class TestingView(FormView):
    template_name = "testing.html"

    def get_form(self, form_class=None):
        import sys
        import inspect
        from . import forms as f

        task_in_session = get_object_or_404(
            M2MTaskInTestingSession, pk=self.kwargs["pk"]
        )
        task = Task.objects.select_derivatives().get(pk=task_in_session.task.pk)
        for _, form_class in inspect.getmembers(sys.modules[f.__name__], inspect.isclass):
            is_task_model_form = hasattr(form_class, "Meta") and hasattr(form_class.Meta, "model") and \
                                 hasattr(form_class.Meta.model, "task_model")
            if is_task_model_form and form_class.Meta.model.task_model == task.__class__:
                if self.request.POST:
                    return form_class(task_in_session, self.request.POST)
                return form_class(task_in_session)

        raise NotImplementedError(
            f"Not implemented ModelForm for class {task.__class__.__name__}"
        )

    def get_success_url(self) -> str:
        return f"session={self.kwargs['pk']}"
