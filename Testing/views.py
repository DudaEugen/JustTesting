from django.http.response import HttpResponseRedirect
from django.views.generic import CreateView
from .models import *


class TestingSessionCreateView(CreateView):
    template_name = "test_session_create.html"
    success_url = "start"

    def get_form(self, form_class=None):
        from django.forms import modelform_factory

        if self.request.user.is_authenticated:
            form_factory = modelform_factory(
                model=TestingSessionOfAutorizedUser,
                fields=["test"],
            )
        else:
            form_factory = modelform_factory(
                model=TestingSessionOfUnautorizedUser,
                fields=["test", "information"],
            )
        if self.request.POST:
            return form_factory(self.request.POST)
        return form_factory()

    def form_valid(self, form) -> HttpResponseRedirect:
        test_session = form.save(commit=False)
        if self.request.user.is_authenticated:
            test_session.user = self.request.user
            test_session.save()
        else:
            test_session.save(self.request.session)
        return HttpResponseRedirect(self.success_url)
