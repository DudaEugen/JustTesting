from django import forms
from django.forms import widgets
from . import models
from Test.models import Test
from Task.models import MultipleChoiceTest, MultipleChoiceTestAnswer
from typing import Dict, Any
from django.utils import timezone


class TestingSessionOfAutorizedUserForm(forms.ModelForm):
    def __init__(self, active_user_sessions, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["test"].queryset = Test.objects.filter(is_allowed=True)
        self.active_user_sessions = active_user_sessions
    
    def clean_test(self):
        if self.cleaned_data["test"].id in {session.test.id for session in self.active_user_sessions}:
            self.add_error(field="test", error="Ви ще не завершили таке тестування, що було розпочато раніше")
            return
        return self.cleaned_data["test"]

    class Meta:
        model = models.TestingSessionOfAutorizedUser
        fields = ["test", "group"]


class TestingSessionOfUnautorizedUserForm(forms.ModelForm):
    def __init__(self, active_user_sessions, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["test"].queryset = Test.objects.filter(
            is_allowed=True, is_allow_for_unautorized_users=True)
        self.active_user_sessions = active_user_sessions
    
    def clean(self) -> Dict[str, Any]:
        cleaned_data = super().clean()
        if len(self.active_user_sessions) > 0:
            self.add_error(field=None, error="Ви маєте незавершенні тестування")
        return cleaned_data

    class Meta:
        model = models.TestingSessionOfUnautorizedUser
        fields = ["test", "display_name", "group"]


class MultipleChoiceTestSolutionForm(forms.Form):
    template_name: str = "Testing/forms/MultipleChoiceTestSolutionForm.html"

    selected_answers = forms.MultipleChoiceField(
        widget=widgets.CheckboxSelectMultiple,
    )

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

    def save(self):
        solution = models.MultipleChoiceTestSolution()
        solution.task_in_testing_session = self.task_in_testing_session
        solution.save()
        for answer in self.cleaned_data['selected_answers']:
            solution.selected_answers.add(MultipleChoiceTestAnswer.objects.get(id=answer))
        solution.compute_and_save_result_if_not_exist()


class ResultsDispatcherForm(forms.Form):
    test = forms.ModelChoiceField(
        queryset=Test.objects.all(),
        required=True,
        label="Тест",
        help_text="Оберіть тест",
    )
    from_date = forms.DateField(
        required=True,
        label="Від",
        initial=timezone.now,
    )
    to_date = forms.DateField(
        required=True,
        label="До",
        initial=timezone.now,
    )
