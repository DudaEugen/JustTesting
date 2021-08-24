from django import forms
from typing import List
from .models import *
from JustTesting.utils.formsets import ModelAndInlineFormsetContainer


class MultipleChoiceTestAnswerInlineFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        answers: List[MultipleChoiceTestAnswer] = []
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data["DELETE"]:
                answer_text = form.cleaned_data.get("text")
                answer_weight = form.cleaned_data.get("weight")
                if answer_text is not None and answer_weight is not None:
                    answers.append(MultipleChoiceTestAnswer(
                        text=answer_text,
                        weight=answer_weight
                    ))
        MultipleChoiceTest.clean_answer_set(answers)


class MultipleChoiceTestWithAnswersForm(ModelAndInlineFormsetContainer):
    model = MultipleChoiceTest
    model_fields = ("task_list", "text", "help_text")
    inline_model = MultipleChoiceTestAnswer
    inline_model_fields = "__all__"
    formset = MultipleChoiceTestAnswerInlineFormset

    @classmethod
    def get_queryset(cls, instance):
        return instance.answer_set.all()
