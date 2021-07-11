from django import forms
from .models import M2MTaskListInTest


class M2MTaskListInTestForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data and not cleaned_data["DELETE"]:
            if cleaned_data["task_list"].task_set.all().count() < cleaned_data["task_count"]:
                raise forms.ValidationError(
                    f"Цей список завдань не має такої кількості завдань")
        return cleaned_data

    class Meta:
        model = M2MTaskListInTest
        fields = ("__all__")
