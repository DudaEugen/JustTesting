from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView, FormView, DetailView, ListView
from django.http import Http404
from .models import *
from .forms import TestingSessionOfAutorizedUserForm, TestingSessionOfUnautorizedUserForm
from django.utils import timezone
from typing import Dict, Any


class TestingSessionCreateView(CreateView):
    template_name = "Testing/test_session_create.html"
    success_url = "start"

    def get_active_sessions(self):
        return TestingSession.get_active_sessions(self.request)

    def get_form(self, form_class=None):
        self.kwargs["active_sessions"] = self.get_active_sessions()
        self.kwargs["active_sessions_count"] = self.kwargs["active_sessions"].count()

        if self.request.user.is_authenticated:
            if self.request.POST:
                return TestingSessionOfAutorizedUserForm(self.kwargs["active_sessions"], self.request.POST)
            return TestingSessionOfAutorizedUserForm(self.kwargs["active_sessions"])
        else:
            if self.request.POST:
                return TestingSessionOfUnautorizedUserForm(self.kwargs["active_sessions"], self.request.POST)
            return TestingSessionOfUnautorizedUserForm(self.kwargs["active_sessions"])

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["active_sessions_count"] = self.kwargs["active_sessions_count"]
        if context["active_sessions_count"] == 1:
            context["session_id"] = self.kwargs["active_sessions"].first().id
        return context

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

    def dispatch(self, request, *args, **kwargs):
        self.kwargs["session"] = self.get_session()
        if self.kwargs["session"].end < timezone.now():
            return HttpResponseRedirect(reverse('testing result', kwargs={'pk': self.kwargs["pk"]}))
        self.kwargs["task_in_session"] = M2MTaskInTestingSession.objects.filter(
            session_id=self.kwargs["session"].id, is_completed=False
        ).first()
        if self.kwargs["task_in_session"] is None:
            return HttpResponseRedirect(reverse('testing result', kwargs={'pk': self.kwargs["pk"]}))
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        task_in_session = self.kwargs["task_in_session"]
        self.kwargs["task"] = Task.objects.select_derivatives().get(
            pk=task_in_session.task.pk)
        self.kwargs["form_class"] = self.get_form_class()
        form_class = self.kwargs["form_class"]

        if not task_in_session.issue_datetime:
            task_in_session.issue_datetime = timezone.now()
            task_in_session.save()
        if self.request.POST:
            return form_class(task_in_session, self.request.POST)
        return form_class(task_in_session)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["session"] = self.kwargs["session"]
        context["number_of_task_left"] = context["session"].task_set.filter(is_completed=False).count()
        return context

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


class TestingResultView(DetailView):
    template_name = "Testing/result.html"

    def get_session(self):
        try:
            session = TestingSession.objects.select_derivatives().get(
                pk=self.kwargs["pk"])
        except TestingSession.DoesNotExist:
            raise Http404("Incorrect session pk")

        if not session.is_correct_user(self.request):
            raise Http404("Incorrect session pk")
        return session

    def dispatch(self, request, *args, **kwargs):
        self.kwargs["session"] = self.get_session()
        try:
            self.kwargs["session"].compute_and_save_result_if_not_exist(
                force_recalculate=self.kwargs["session"].result is None and\
                                  self.kwargs["session"].end < timezone.now()
            )
        except RuntimeError:
            if self.kwargs["session"].end > timezone.now():
                return HttpResponseRedirect(reverse('testing', kwargs={'pk': self.kwargs["pk"]}))
            return HttpResponseRedirect(reverse('create testing session'))
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.kwargs["session"]


class ActiveTestingSessions(ListView):
    model = TestingSessionOfAutorizedUser
    template_name = "Testing/active_testing_sessions.html"
    context_object_name = "sessions"

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            raise Http404("Not authenticated user can't have more than 1 session")
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        return TestingSessionOfAutorizedUser.get_active_sessions(self.request)
