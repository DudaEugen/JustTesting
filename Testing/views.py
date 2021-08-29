from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView, FormView, DetailView, ListView, RedirectView
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import *
from .forms import TestingSessionOfAutorizedUserForm, TestingSessionOfUnautorizedUserForm,\
                   ResultsDispatcherForm
from django.utils import timezone
from typing import Dict, Any, Tuple


class TestingSessionCreateView(CreateView):
    template_name = "Testing/test_session_create.html"
    success_url = "start"

    def get_initial(self) -> Dict[str, Any]:
        initial_test = self.kwargs.get("test_pk")
        return {} if initial_test is None else {"test": initial_test}

    def get_active_sessions(self):
        return TestingSession.get_active_sessions(self.request)

    def get_form(self, form_class=None):
        self.kwargs["active_sessions"] = self.get_active_sessions()
        self.kwargs["active_sessions_count"] = self.kwargs["active_sessions"].count()

        if self.request.user.is_authenticated:
            if self.request.POST:
                return TestingSessionOfAutorizedUserForm(self.kwargs["active_sessions"], self.request.POST,
                        initial=self.get_initial())
            return TestingSessionOfAutorizedUserForm(self.kwargs["active_sessions"], 
                    initial=self.get_initial())
        else:
            if self.request.POST:
                return TestingSessionOfUnautorizedUserForm(self.kwargs["active_sessions"],
                        self.get_client_ip(), self.request.POST, initial=self.get_initial())
            return TestingSessionOfUnautorizedUserForm(self.kwargs["active_sessions"], 
                    self.get_client_ip(), initial=self.get_initial())

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
            test_session.ip_begin = self.get_client_ip()
            test_session.save(self.request.session)
        self.kwargs["session"] = test_session
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self) -> str:
        return f"session={self.kwargs['session'].pk}"

    def get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip


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
            session_id=self.kwargs["session"].id, is_completed=False, task__isnull=False
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
        context["number_of_task_left"] = context["session"].task_set.filter(
            is_completed=False, task__isnull=False
        ).count()
        if context["session"].test.is_allow_help:
            context["help"] = self.kwargs["task"].help_text
        return context

    def form_valid(self, form):
        self.kwargs["solution"] = form.save()
        if self.kwargs["session"].test.repeat_unresolved_tasks and self.kwargs["solution"].result != 100:
            self.kwargs["solution"].task_in_testing_session.replace_to_end()
            self.kwargs["solution"].task_in_testing_session.save()
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
        if self.kwargs["session"].test.show_right_solution_after_mistake and\
           self.kwargs["solution"].result != 100:
            return reverse("right solution", kwargs={
                "session_pk": self.kwargs["session"].id,
                "solution_pk":  self.kwargs["solution"].id,
            })
        return reverse("testing", kwargs={"pk": self.kwargs['pk']})


class CloseTestingSessionView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        testing_session = TestingSession.objects.select_derivatives().get(pk=self.kwargs["pk"])
        if not testing_session.is_correct_user(self.request):
            raise Http404("It is not your session")
        testing_session.compute_and_save_result_if_not_exist(
            force_recalculate=testing_session.result is None
        )
        self.url = 'result'    
        return super().get_redirect_url(*args, **kwargs)


class RightSolutionView(DetailView):
    templates_dir_name = "right_solutions"
    context_object_name = "solution"

    def get_session(self):
        try:
            session = TestingSession.objects.select_derivatives().get(pk=self.kwargs["session_pk"])
        except TestingSession.DoesNotExist:
            raise Http404("Incorrect session pk")

        if not session.is_correct_user(self.request):
            raise Http404("Incorrect session pk")
        return session
    
    def get_task(self):
        from Task.models import Task

        return Task.objects.select_derivatives().filter(
            id=self.kwargs["solution"].task_in_testing_session.task.id
        ).first()

    def get_object(self, queryset=None):
        session = self.get_session()
        try:
            self.kwargs["solution"] = Solution.objects.select_derivatives().get(
                pk=self.kwargs["solution_pk"], task_in_testing_session__session=session
            )
        except Solution.DoesNotExist:
            raise Http404("Incorrect solution pk") 
        self.kwargs["template_name"] = self.kwargs['solution'].task_model.__name__
        if self.kwargs["solution"].datetime < timezone.now() - timezone.timedelta(minutes=1):
            self.kwargs["solution"] = None
        return self.kwargs["solution"]

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["session_pk"] = self.kwargs["session_pk"]
        if self.kwargs["solution"] is not None:
            context["task"] = self.get_task()
        return context

    def get_template_names(self):
        return [
            f"Testing/{RightSolutionView.templates_dir_name}/{self.kwargs['template_name']}.html"
        ]


class SkipTaskView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        testing_session = TestingSession.objects.select_derivatives().get(pk=self.kwargs["session_pk"])
        if not testing_session.is_correct_user(self.request):
            raise Http404("It is not your session")
        if not testing_session.test.is_allow_skip_task:
            self.url = reverse("testing", kwargs={"pk": testing_session.id})
        else:
            task_in_session = M2MTaskInTestingSession.objects.filter(
                session_id=self.kwargs["session_pk"], is_completed=False, task__isnull=False
            ).first()
            if task_in_session is None:
                self.url = reverse("testing result", kwargs={"pk": testing_session.id})
            else:
                task_in_session.order += 1
                task_in_session.save()
                self.url = reverse("testing", kwargs={"pk": testing_session.id})
        return self.url


class TestingResultView(DetailView):
    template_name = "Testing/result.html"

    def get_session(self):
        try:
            session = TestingSession.objects.select_derivatives().get(
                pk=self.kwargs["pk"])
        except TestingSession.DoesNotExist:
            raise Http404("Incorrect session pk")

        if not session.is_correct_user(self.request) and not (self.request.user.is_authenticated and 
                self.request.user.has_perm("Testing.view_testingsession")):
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


class ResultsDispatcherView(FormView):
    template_name = "Testing/results_dispatcher.html"
    form_class = ResultsDispatcherForm

    def dispatch(self, request, *args: Any, **kwargs: Any):
        if not (self.request.user.is_authenticated and 
                self.request.user.has_perm("Testing.view_testingsession")):
            raise Http404("You don't have permissions for view this page")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        fd = form.cleaned_data["from_date"]
        td = form.cleaned_data["to_date"]
        return HttpResponseRedirect(reverse("testing results", kwargs={
            "test_pk": form.cleaned_data["test"].id,
            "from": f"{fd.day:02d}.{fd.month:02d}.{fd.year}",
            "to": f"{td.day:02d}.{td.month:02d}.{td.year}",
        }))


class ResultsView(ListView):
    template_name = "Testing/results.html"
    context_object_name = "sessions"

    def dispatch(self, request, *args: Any, **kwargs: Any):
        if not (self.request.user.is_authenticated and 
                self.request.user.has_perm("Testing.view_testingsession")):
            raise Http404("You don't have permissions for view this page")
        return super().dispatch(request, *args, **kwargs)

    def get_dates(self) -> Tuple[timezone.datetime, timezone.datetime]:
        from django.utils.timezone import make_aware

        from_date = self.kwargs["from"]
        to_date = self.kwargs["to"]
        return (
            make_aware(timezone.datetime(
                day=int(from_date[:2]), month=int(from_date[3:5]), year=int(from_date[6:])
            )), 
            make_aware(timezone.datetime(
                day=int(to_date[:2]), month=int(to_date[3:5]), year=int(to_date[6:]), 
                hour=23, minute=59, second=59
            ))
        )

    def get_queryset(self):
        begin_date, end_date = self.get_dates()
        self.kwargs["test"] = get_object_or_404(Test, id=self.kwargs["test_pk"])

        sessions = TestingSession.objects.select_derivatives().filter(
            test_id=self.kwargs["test"].id, begin__gte=begin_date
        ).filter(
            Q(end__lte=end_date) & Q(end__lte=timezone.now()) | Q(result__isnull=False)
        ).order_by("-end")
        for session in sessions:
            session.compute_and_save_result_if_not_exist(force_recalculate=session.result is None)
        return sessions
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["test"] = self.kwargs["test"]
        dates = self.get_dates()
        context["from_date"] = dates[0]
        context["to_date"] = dates[1]
        return context
