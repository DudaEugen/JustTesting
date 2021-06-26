from django import forms
from typing import List, Optional

from django.forms import fields
from .models import *


class MultiplyChoiceTestAnswerInlineFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        answers: List[MultiplyChoiceTestAnswer] = []
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data["DELETE"]:
                answers.append(MultiplyChoiceTestAnswer(
                    text=form.cleaned_data["text"],
                    weight=form.cleaned_data["weight"]
                ))
        errors: Optional[str] = MultiplyChoiceTest.find_errors_in_answer_list(
            answers
        )
        print(errors)
        if errors is not None:
            raise forms.ValidationError(errors)


class MultiplyChoiceTestForm(forms.ModelForm):
    class Meta:
        model = MultiplyChoiceTest
        fields = ("task_list", "text")


class MultiplyChoiceTestWithAnswersForm:
    def __init__(self, **kwargs):
        self.test_form = MultiplyChoiceTestForm(**kwargs)
        answers_formset_factory = forms.inlineformset_factory(
            MultiplyChoiceTest,
            MultiplyChoiceTestAnswer,
            formset=MultiplyChoiceTestAnswerInlineFormset,
            fields=("text", "weight"),
            extra=2,
        )
        self.answer_formset = answers_formset_factory(
            queryset=MultiplyChoiceTestAnswer.objects.none(), **kwargs
        )

    def is_valid(self):
        return self.test_form.is_valid() and self.answer_formset.is_valid()

    def save(self, commit: bool = True):
        test_cd = self.test_form.cleaned_data
        new_test = MultiplyChoiceTest(
            task_list=test_cd.get("task_list"), text=test_cd.get("text")
        )
        new_test.save()
        for form in self.answer_formset:
            cd = form.cleaned_data
            answer = MultiplyChoiceTestAnswer(
                test=new_test, text=cd.get("text"), weight=cd.get("weight")
            )
            answer.save()
