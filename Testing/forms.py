from django import forms
from django.forms import widgets
from . import models


class MultipleChoiceTestSolutionForm(forms.ModelForm):
    def __init__(self, task_in_session: models.M2MTaskInTestingSession,  *args, **kwargs):
        import random

        super().__init__(*args, **kwargs)
        self.task_in_testing_session = task_in_session
        self.fields["selected_answers"].choices = [
            (option.id, option.text) for option in
            self.task_in_testing_session.task.multiplechoicetest.answer_set.all()
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
