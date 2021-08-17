from django.http.response import HttpResponseRedirect
from django.views.generic import CreateView, FormView
from django.http import Http404
from .models import *
from .forms import TestingSessionOfAutorizedUserForm, TestingSessionOfUnautorizedUserForm
from django.utils import timezone


class TestingSessionCreateView(CreateView):
    template_name = "Testing/test_session_create.html"
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
    def get_session(self):
        try:
            session = TestingSession.objects.select_derivatives().get(
                pk=self.kwargs["pk"])
        except TestingSession.DoesNotExist:
            raise Http404("Incorrect session pk")

        if not session.is_correct_user(self.request):
            raise Http404("Incorrect session pk")
        return session

    def get_form(self, form_class=None):
        self.kwargs["session"] = self.get_session()
        task_in_session = M2MTaskInTestingSession.objects.filter(
            session_id=self.kwargs["session"].id, is_completed=False
        ).first()
        if task_in_session is None:
            raise Http404("Incorrect session pk")

        self.kwargs["task"] = Task.objects.select_derivatives().get(pk=task_in_session.task.pk)
        self.kwargs["form_class"] = self.get_form_class()
        form_class = self.kwargs["form_class"]

        if not task_in_session.issue_datetime:
            task_in_session.issue_datetime = timezone.now()
            task_in_session.save()
        if self.request.POST:
            return form_class(task_in_session, self.request.POST)
        return form_class(task_in_session)

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_form_class(self):
        task = self.kwargs["task"]
        for solution_class in Solution.__subclasses__():
            if solution_class.task_model == task.__class__:
                return solution_class.task_form
        raise NotImplementedError(
            f"Not implemented Form for class {task.__class__.__name__}"
        )

    def get_template_names(self):
        return [self.kwargs["form_class"].template_name]

    def get_success_url(self) -> str:
        return f"session={self.kwargs['pk']}"
