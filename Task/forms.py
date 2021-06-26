from django import forms
from typing import List, Optional


class MultiplyChoiceTestAnswerInlineFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        from .models import MultiplyChoiceTest, MultiplyChoiceTestAnswer

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
