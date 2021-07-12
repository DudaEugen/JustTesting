from django import forms
from typing import List
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
        MultiplyChoiceTest.clean_answer_set(answers)


class MultiplyChoiceTestWithAnswersForm(ModelAndInlineFormsetContainer):
    model = MultiplyChoiceTest
    model_fields = ("task_list", "text")
    inline_model = MultiplyChoiceTestAnswer
    inline_model_fields = "__all__"
    formset = MultiplyChoiceTestAnswerInlineFormset

    @classmethod
    def get_queryset(cls, instance):
        return instance.answer_set.all()
