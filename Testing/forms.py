from django import forms
from django.forms import widgets
from . import models
from Test.models import Test
from Task.models import MultipleChoiceTest


class TestingSessionOfAutorizedUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["test"].queryset = Test.objects.filter(is_allowed=True)

    class Meta:
        model = models.TestingSessionOfAutorizedUser
        fields = ["test"]


class TestingSessionOfUnautorizedUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["test"].queryset = Test.objects.filter(is_allowed=True, is_allow_for_unautorized_users=True)

    class Meta:
        model = models.TestingSessionOfUnautorizedUser
        fields = ["test", "information"]


class MultipleChoiceTestSolutionForm(forms.ModelForm):
    template_name: str = "Testing/forms/MultipleChoiceTestSolutionForm.html"

    def __init__(self, task_in_session: models.M2MTaskInTestingSession,  *args, **kwargs):
        import random

        super().__init__(*args, **kwargs)
        self.task_in_testing_session = task_in_session
        multiple_choice_test: MultipleChoiceTest = self.task_in_testing_session.task.multiplechoicetest
        self.fields["selected_answers"].label = multiple_choice_test.text
        self.fields["selected_answers"].choices = [
            (option.id, option.text) for option in multiple_choice_test.answer_set.all()
        ]
        random.shuffle(self.fields["selected_answers"].choices)

    def save(self, commit: bool = True):
        solution = super().save(False)
        solution.task_in_testing_session = self.task_in_testing_session
        solution.save(commit)

    class Meta:
        model = models.MultipleChoiceTestSolution
        fields = ("selected_answers",)
        widgets = {"selected_answers": widgets.CheckboxSelectMultiple}
