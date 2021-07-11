from django import forms
from .models import M2MTaskListInTest, Test
from JustTesting.utils.formsets import ModelAndInlineFormsetContainer


class M2MTaskListInTestForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data and not cleaned_data["DELETE"]:
            max_count: int = cleaned_data["task_list"].task_set.all().count()
            if max_count < cleaned_data["task_count"]:
                raise forms.ValidationError(
                    f'Cписок завдань "{cleaned_data["task_list"].name}" містить всього '
                    f'{max_count} завдань. Тому з цього списку не можна взяти '
                    f'{cleaned_data["task_count"]} завдань.'
                )
        return cleaned_data

    class Meta:
        model = M2MTaskListInTest
        fields = ("__all__")


class TestWithTaskListForm(ModelAndInlineFormsetContainer):
    model = Test
    model_fields = (
        "name",
        "duration",
        "is_allowed",
        "is_allow_for_unautorized_users",
    )
    inline_model = M2MTaskListInTest
    inline_model_fields = "__all__"
    inline_form = M2MTaskListInTestForm

    @classmethod
    def get_queryset(cls, instance):
        return instance.m2mtasklistintest_set.all()
