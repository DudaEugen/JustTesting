from django import forms
from typing import List, Optional
from .models import *
from JustTesting.utils.formsets import ModelAndInlineFormsetContainer


class MultiplyChoiceTestAnswerInlineFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        answers: List[MultiplyChoiceTestAnswer] = []
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data["DELETE"]:
                answer_text = form.cleaned_data.get("text")
                answer_weight = form.cleaned_data.get("weight")
                if answer_text is not None and answer_weight is not None:
                    answers.append(MultiplyChoiceTestAnswer(
                        text=answer_text,
                        weight=answer_weight
                    ))
        errors: Optional[str] = MultiplyChoiceTest.find_errors_in_answer_list(
            answers
        )
        if errors is not None:
            raise forms.ValidationError(errors)


class MultiplyChoiceTestWithAnswersForm(ModelAndInlineFormsetContainer):
    model = MultiplyChoiceTest
    model_fields = ("task_list", "text")
    formset_model = MultiplyChoiceTestAnswer
    formset_model_fields = "__all__"
    formset = MultiplyChoiceTestAnswerInlineFormset
    formset_model_foreignkey_name = "test"

    @classmethod
    def get_queryset(cls, instance):
        return instance.answer_set.all()
