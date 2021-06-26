from django import forms
from typing import List, Optional
from .models import *
from JustTesting.utils.formsets import ModelAndInlineFormsetContainer


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


class MultiplyChoiceTestWithAnswersForm(ModelAndInlineFormsetContainer):
    model = MultiplyChoiceTest
    model_fields = ("task_list", "text")
    formset_model = MultiplyChoiceTestAnswer
    formset_model_fields = ("text", "weight")
    formset = MultiplyChoiceTestAnswerInlineFormset
    formset_model_foreignkey_name = "test"
